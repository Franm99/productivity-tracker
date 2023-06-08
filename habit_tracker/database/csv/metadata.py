import pathlib

from pydantic import BaseModel


class DBMetadata(BaseModel):
    name: str
    activities: list[str]
    par_dir: pathlib.Path

    @property
    def db_path(self) -> pathlib.Path:
        return self.par_dir / pathlib.Path(self.name)

    @property
    def file(self) -> pathlib.Path:
        return self.db_path / pathlib.Path("metadata.json")
