from src.worker import compute_hash_by_file


def test_simple_md5() -> None:
    result = compute_hash_by_file.run(file="aaaaaaaaaaaaaaaaaa", hash_type="md5")

    assert "hash" in result
    assert result["hash"] == "2c60c24e7087e18e45055a33f9a5be91"
