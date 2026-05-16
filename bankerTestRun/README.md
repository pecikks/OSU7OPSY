# Banker Test Run

This project is a simple console simulation of the Banker's algorithm. It checks whether resource allocation requests from clients can be safely approved without leading to an unsafe state or possible deadlock.

The program asks for the banker's total available resources, then collects maximum and currently allocated resources for four clients. After validating the initial state, it lets the user enter new resource requests. Each request is approved only if it does not exceed the client's remaining need, does not exceed currently available resources, and keeps the system in a safe state.

## Files

- `banker.py` - main Python script with the Banker's algorithm simulation.
- `banker.spec` - PyInstaller configuration used to build the executable.
- `dist/banker.exe` - built Windows executable.

## Run

Run the Python script:

```powershell
python banker.py
```

Or run the built executable:

```powershell
.\dist\banker.exe
```

## Build

If PyInstaller is installed, the executable can be rebuilt with:

```powershell
pyinstaller banker.spec
```
