@echo off

echo ========================================
echo   MONITORAMENTO DE QUALIDADE DE DADOS
echo ========================================
echo.

echo [1/2] Carregando dados no PostgreSQL...
python src\carregar_dados.py

if errorlevel 1 (
    echo.
    echo ERRO: Falha ao carregar os dados.
    pause
    exit /b 1
)

echo.
echo [2/2] Executando monitoramento...
python src\main.py

if errorlevel 1 (
    echo.
    echo ERRO: Falha durante o monitoramento.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   MONITORAMENTO CONCLUIDO
echo ========================================
pause
