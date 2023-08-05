from __future__ import annotations

import abc
import contextlib
import dataclasses
import datetime
import enum
import hashlib
import json
import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any, Iterator, NoReturn, Sequence

from kraken.util.helpers import NotSet, not_none

if TYPE_CHECKING:
    from kraken.util.requirements import RequirementSpec

    from kraken.wrapper.lockfile import Lockfile

logger = logging.getLogger(__name__)


@dataclasses.dataclass(frozen=True)
class Distribution:
    name: str
    version: str
    requirements: list[str]
    extras: set[str]


class BuildEnv(abc.ABC):
    """Interface for the build environment."""

    @abc.abstractmethod
    def get_type(self) -> BuildEnvType:
        """Return the type of build environment that this is."""

    @abc.abstractmethod
    def get_path(self) -> Path:
        """Return the path to the build environment."""

    @abc.abstractmethod
    def get_installed_distributions(self) -> list[Distribution]:
        """Return the distributions that are currently installed in the environment."""

    @abc.abstractmethod
    def build(self, requirements: RequirementSpec) -> None:
        """Build the environment from the given requirement spec."""

    @abc.abstractmethod
    def dispatch_to_kraken_cli(self, argv: list[str]) -> NoReturn:
        """Dispatch the kraken cli command in *argv* to the build environment.

        :param argv: The arguments to pass to the kraken cli (without the "kraken" command name itself)."""


class BuildEnvType(enum.Enum):
    PEX_ZIPAPP = enum.auto()
    PEX_PACKED = enum.auto()
    PEX_LOOSE = enum.auto()
    VENV = enum.auto()


@dataclasses.dataclass(frozen=True)
class BuildEnvMetadata:
    created_at: datetime.datetime
    environment_type: BuildEnvType
    requirements_hash: str
    hash_algorithm: str

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> BuildEnvMetadata:
        from kraken.util.json import json2dt

        return cls(
            created_at=json2dt(data["created_at"]),
            environment_type=BuildEnvType[data["environment_type"]],
            requirements_hash=data["requirements_hash"],
            hash_algorithm=data["hash_algorithm"],
        )

    def to_json(self) -> dict[str, Any]:
        from kraken.util.json import dt2json

        return {
            "created_at": dt2json(self.created_at),
            "environment_type": self.environment_type.name,
            "requirements_hash": self.requirements_hash,
            "hash_algorithm": self.hash_algorithm,
        }


@dataclasses.dataclass
class BuildEnvMetadataStore:
    path: Path

    def __post_init__(self) -> None:
        self._metadata: BuildEnvMetadata | None | NotSet = NotSet.Value

    def get(self) -> BuildEnvMetadata | None:
        if self._metadata is NotSet.Value:
            if self.path.is_file():
                self._metadata = BuildEnvMetadata.from_json(json.loads(self.path.read_text()))
            else:
                self._metadata = None
        return self._metadata

    def set(self, metadata: BuildEnvMetadata) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(metadata.to_json()))
        self._metadata = metadata


class PexBuildEnv(BuildEnv):
    STYLES = (BuildEnvType.PEX_ZIPAPP, BuildEnvType.PEX_PACKED, BuildEnvType.PEX_LOOSE)

    def __init__(self, style: BuildEnvType, path: Path) -> None:
        assert style in self.STYLES
        self._style = style
        self._path = path

    @contextlib.contextmanager
    def activate(self) -> Iterator[None]:
        import copy

        from pex.pex import PEX
        from pex.pex_bootstrapper import bootstrap_pex_env

        assert self._path.exists(), f'expected PEX file at "{self._path}"'
        pex = PEX(self._path)

        state = {}
        for key in ["displayhook", "excepthook", "modules", "path", "path_importer_cache"]:
            state[key] = copy.copy(getattr(sys, key))

        try:
            bootstrap_pex_env(str(pex.path()))
            pex.activate()
            yield
        finally:
            for key, value in state.items():
                setattr(sys, key, value)

    # BuildEnv

    def get_path(self) -> Path:
        return self._path

    def get_type(self) -> BuildEnvType:
        return self._style

    def get_installed_distributions(self) -> list[Distribution]:
        return _get_installed_distributions([sys.executable, str(self._path)])

    def build(self, requirements: RequirementSpec) -> None:
        import pprint

        from kraken.util.text import lazy_str

        from kraken.wrapper.pex import PEXBuildConfig, PEXLayout

        config = PEXBuildConfig(
            interpreter_constraints=(
                [requirements.interpreter_constraint] if requirements.interpreter_constraint else []
            ),
            script="kraken",
            requirements=requirements.to_args(Path.cwd(), with_options=False),
            index_url=requirements.index_url,
            extra_index_urls=list(requirements.extra_index_urls),
        )

        layout = {
            BuildEnvType.PEX_ZIPAPP: PEXLayout.ZIPAPP,
            BuildEnvType.PEX_PACKED: PEXLayout.PACKED,
            BuildEnvType.PEX_LOOSE: PEXLayout.LOOSE,
        }[self._style]

        logger.debug("PEX build configuration is %s", lazy_str(lambda: pprint.pformat(config)))

        logger.info('begin PEX resolve for build environment "%s"', self._path)
        installed = config.resolve()

        logger.info('building PEX for build environment "%s"', self._path)
        builder = config.builder(installed)
        builder.build(str(self._path), layout=layout)

    def dispatch_to_kraken_cli(self, argv: list[str]) -> NoReturn:
        from kraken.util.krakenw import KrakenwEnv

        with self.activate():
            from kraken.cli.main import main

            env = os.environ.copy()
            os.environ.update(KrakenwEnv(self._path, self.get_type().name).to_env_vars())
            try:
                main("krakenw", argv)
            finally:
                os.environ.clear()
                os.environ.update(env)
        assert False


class VenvBuildEnv(BuildEnv):
    def __init__(self, path: Path) -> None:
        from kraken._vendor.nr.python.environment.virtualenv import VirtualEnvInfo

        self._path = path
        self._venv = VirtualEnvInfo(self._path)

    # BuildEnv

    def get_path(self) -> Path:
        return self._path

    def get_type(self) -> BuildEnvType:
        return BuildEnvType.VENV

    def get_installed_distributions(self) -> list[Distribution]:
        python = self._venv.get_bin("python")
        return _get_installed_distributions([str(python), "-m", "kraken.cli.main"])

    def build(self, requirements: RequirementSpec) -> None:
        command = [sys.executable, "-m", "venv", str(self._path)]
        subprocess.check_call(command)

        python_bin = str(self._venv.get_bin("python"))
        command = [python_bin, "-m", "pip", "install", "--use-feature=in-tree-build", *requirements.to_args()]
        subprocess.check_call(command)

        # Make sure the pythonpath from the requirements is encoded into the enviroment.
        if requirements.pythonpath:
            command = [python_bin, "-c", "from sysconfig import get_path; print(get_path('purelib'))"]
            site_packages = Path(subprocess.check_output(command).decode().strip())
            pth_file = site_packages / "krakenw.pth"
            pth_file.write_text("\n".join(str(Path(path).absolute()) for path in requirements.pythonpath))

    def dispatch_to_kraken_cli(self, argv: list[str]) -> NoReturn:
        from kraken.util.krakenw import KrakenwEnv

        python = self._venv.get_bin("python")
        command = [str(python), "-m", "kraken.cli.main", *argv]
        env = {**os.environ, **KrakenwEnv(self._path, self.get_type().name).to_env_vars()}
        sys.exit(subprocess.call(command, env=env))


class BuildEnvManager:
    def __init__(
        self,
        path: Path,
        default_type: BuildEnvType = BuildEnvType.PEX_ZIPAPP,
        default_hash_algorithm: str = "sha256",
    ) -> None:
        from kraken.util.path import with_name

        assert (
            default_hash_algorithm in hashlib.algorithms_available
        ), f"hash algoritm {default_hash_algorithm!r} is not available"

        self._path = path
        self._metadata_store = BuildEnvMetadataStore(with_name(path, path.name + ".meta"))
        self._default_type = default_type
        self._default_hash_algorithm = default_hash_algorithm

    def exists(self) -> bool:
        if self._metadata_store.get() is None:
            return False  # If we don't have metadata, we assume the environment does not exist.
        return self.get_environment().get_path().exists()

    def remove(self) -> None:
        from kraken.util.fs import safe_rmpath

        safe_rmpath(self._metadata_store.path)
        safe_rmpath(self.get_environment().get_path())

    def install(self, requirements: RequirementSpec, env_type: BuildEnvType | None = None) -> None:
        if env_type is None:
            metadata = self._metadata_store.get()
            env_type = metadata.environment_type if metadata else self._default_type

        env = _get_environment_for_type(env_type, self._path)
        env.build(requirements)
        hash_algorithm = self.get_hash_algorithm()
        metadata = BuildEnvMetadata(
            datetime.datetime.utcnow(),
            env.get_type(),
            requirements.to_hash(hash_algorithm),
            hash_algorithm,
        )
        self._metadata_store.set(metadata)

    def get_metadata_file(self) -> Path:
        return self._metadata_store.path

    def get_metadata(self) -> BuildEnvMetadata:
        return not_none(self._metadata_store.get(), "metadata does not exist")

    def get_hash_algorithm(self) -> str:
        metadata = self._metadata_store.get()
        return metadata.hash_algorithm if metadata else self._default_hash_algorithm

    def get_environment(self) -> BuildEnv:
        metadata = self._metadata_store.get()
        environment_type = self._default_type if metadata is None else metadata.environment_type
        return _get_environment_for_type(environment_type, self._path)

    def set_locked(self, lockfile: Lockfile) -> None:
        metadata = self._metadata_store.get()
        assert metadata is not None
        metadata = BuildEnvMetadata(
            metadata.created_at,
            metadata.environment_type,
            lockfile.to_pinned_requirement_spec().to_hash(metadata.hash_algorithm),
            metadata.hash_algorithm,
        )
        self._metadata_store.set(metadata)


def _get_environment_for_type(environment_type: BuildEnvType, base_path: Path) -> BuildEnv:
    from kraken.util.path import with_name

    if environment_type in PexBuildEnv.STYLES:
        return PexBuildEnv(environment_type, with_name(base_path, base_path.name + ".pex"))
    elif environment_type == BuildEnvType.VENV:
        return VenvBuildEnv(base_path)
    else:
        raise RuntimeError(f"unsupported environment type: {environment_type!r}")


def _get_installed_distributions(kraken_command_prefix: Sequence[str]) -> list[Distribution]:
    command = [*kraken_command_prefix, "query", "env"]
    output = subprocess.check_output(command).decode()
    return [Distribution(x["name"], x["version"], x["requirements"], x["extras"]) for x in json.loads(output)]
