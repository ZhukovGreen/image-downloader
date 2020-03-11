import pathlib

import pytest

from image_downloader import app
from image_downloader.console import main

TEST_DIR = pathlib.Path(__file__).parent


def test_basic(cli_runner, tmp_path):
    # test proper inputs
    result = cli_runner.invoke(
        main,
        ["-v", str(TEST_DIR / "sample_input.txt"), str(tmp_path)],
        catch_exceptions=True,
    )
    assert result.exit_code == 0

    # test not existing file
    result = cli_runner.invoke(
        main,
        ["-v", str("not existing file"), str(tmp_path)],
        catch_exceptions=True,
    )

    assert result.exit_code == 2
    assert "not existing file" in result.stdout

    # test not existing output dir
    result = cli_runner.invoke(
        main,
        ["-v", str(TEST_DIR / "sample_input.txt"), str("not existing dir")],
        catch_exceptions=True,
    )
    assert result.exit_code == 2
    assert "does not exist" in result.stdout

    # test output is a file
    tmp_file = tmp_path / "temp.txt"
    tmp_file.touch()
    result = cli_runner.invoke(
        main,
        ["-v", str(TEST_DIR / "sample_input.txt"), str(tmp_file)],
        catch_exceptions=True,
    )
    assert result.exit_code == 2
    assert "Target should be a directory" in result.stdout


@pytest.mark.asyncio
async def test_bad_inputs(tmp_path, caplog):
    # testing bad urls
    with caplog.at_level("INFO"):
        await app(TEST_DIR / "sample_bad_input.txt", tmp_path)
    assert (
        sum("is not valid" in entry[2] for entry in caplog.record_tuples) == 2
    )

    # testing empty file
    await app(TEST_DIR / "empty.txt", tmp_path)
