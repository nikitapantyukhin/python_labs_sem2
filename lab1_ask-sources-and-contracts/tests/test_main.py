from src.main import main


def test_main_execution(capsys):
    main()

    captured = capsys.readouterr()
    output = captured.out

    assert "ID:" in output
    assert "Payload:" in output