# Android Mobile E2E Tests

> One of my real projects; all real & sensitive data are replaced with placeholders.

## TL;DR

* Python + Pytest-based end‑to‑end tests for an Android app
* Runs on Sauce Labs (real device) **and** in CI (Docker + GitLab CI, optional - locally)
* Simple structure: `core/` (framework), `tests/` (suites & fixtures), `reporting/` (reports & collectors), `tools/` (helpers & scripts)

---

## Features

* **Cross‑environment runs**: local Android emulator/device, or remote device clouds (e.g., Sauce Labs)
* **Headless CI** via Docker and `.gitlab-ci.yml`
* **Parameterized test runs** through `pytest` CLI args and environment variables
* **Artifacts & reports** stored in `reporting/` (JUnit XML, logs; optional Allure if enabled)
* **Utilities**: scripts to prepare data, clean up remote storage, and collect results (see `tools/`)

> All proprietary names, credentials and URLs are masked with placeholders – replace them for your org.

---

## Tech Stack

* **Language**: Python 3.10+
* **Test runner**: Pytest
* **Mobile automation**: Appium (Android)
* **Containerization**: Docker
* **CI**: GitLab CI
* **Optional**: Sauce Labs for hosted devices

> See `requirements.txt` for exact library versions.

---

## Repository Structure

```
.
├── core/                 # framework: drivers, base classes, page objects, config
├── reporting/            # reports, result collectors, JUnit XML, screenshots, logs
├── tests/                # test suites, fixtures, test data
├── tools/                # helper scripts (data seeding, APK ops, utilities)
├── Dockerfile            # container for CI/local reproducible runs
├── pytest.ini            # Pytest configuration, markers, addopts
├── .gitlab-ci.yml        # GitLab pipeline definition
├── ResultCollector.py    # helper for aggregating run outputs
├── avd_config*.ini       # example AVD configs for local emulator
├── requirements.txt      # Python deps
└── README.md
```

---

## Prerequisites (local)

1. **Python** 3.10+ (recommended 3.11)
2. **Java JDK** 11+
3. **Android SDK** with platform‑tools and an emulator image (or a real device with USB debugging)
4. **Appium Server** (Appium 2.x recommended) and drivers for Android
5. **ADB** available in your PATH

> Or skip most of the above by using the **Docker** workflow below.

---

## Quick Start (local)

```bash
# 1) Clone
git clone https://github.com/bikmax/android_mobile_e2e.git
cd android_mobile_e2e

# 2) Create & activate venv
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate

# 3) Install deps
pip install -r requirements.txt

# 4) Export minimal env vars (examples below) and run
pytest -q
```

### Common environment variables

These control the Appium session and target under test.

```bash
# Device / platform
export PLATFORM_NAME=Android
export PLATFORM_VERSION=13
export DEVICE_NAME="emulator-5554"   # or a real device id from `adb devices`

# App under test
export APP_PATH="/abs/path/to/app-debug.apk" # or use APP_PACKAGE & APP_ACTIVITY for installed app
export APP_PACKAGE="com.example.app"
export APP_ACTIVITY=".MainActivity"

# Appium connection
export APPIUM_SERVER_URL="http://127.0.0.1:4723"

# Remote cloud (optional)
export SAUCE_USERNAME="<your-username>"
export SAUCE_ACCESS_KEY="<your-key>"
```

### Running tests

```bash
# Run all tests
pytest

# Run only smoke (marker defined in pytest.ini)
pytest -m smoke

# Verbose + show live logs
pytest -vv -s

# Run a specific test module or node
pytest tests/test_login.py::test_happy_path
```

> Markers and `addopts` are configured in `pytest.ini`. Adjust to your needs.

---

## Docker Workflow

Using the provided `Dockerfile` you can build a reproducible test image for CI or local runs.

```bash
# Build image
docker build -t android-e2e:latest .

# Run tests inside the container (mount reports out)
 docker run --rm \
  -e APPIUM_SERVER_URL \
  -e APP_PATH \
  -e APP_PACKAGE -e APP_ACTIVITY \
  -e PLATFORM_NAME -e PLATFORM_VERSION -e DEVICE_NAME \
  -e SAUCE_USERNAME -e SAUCE_ACCESS_KEY \
  -v "$PWD/reporting:/work/reporting" \
  android-e2e:latest pytest -m smoke -vv
```

> In CI, the emulator/device is usually provided by the runner or a device cloud. For local emulator inside Docker, you’ll need privileged runs and hardware acceleration; prefer running Appium/emulator outside the container and point the container to it via `APPIUM_SERVER_URL`.

---

## Continuous Integration (GitLab)

The pipeline is defined in `.gitlab-ci.yml` and typically includes stages like:

* **prepare** – set up Python deps & environment
* **test** – run `pytest`, produce JUnit XML and artifacts into `reporting/`
* **report** – publish or archive reports (e.g., JUnit, Allure, HTML)

Provide the following CI variables as masked/secret variables:

* `APPIUM_SERVER_URL`
* `APP_PATH` or (`APP_PACKAGE` + `APP_ACTIVITY`)
* `SAUCE_USERNAME`, `SAUCE_ACCESS_KEY` (if using Sauce Labs)

Artifacts (XML, logs, screenshots) are stored under `reporting/` and exposed in job artifacts.

---

## Reports
* **TELEGRAM** – produced by TelegramReport.py

---

## Tools & Utilities

Some useful scripts in the repo (names may vary):

* `tools/` – general helpers for data prep, device operations
* `delete_apk_from_sauce.py` – example of cleaning APKs from Sauce Storage
* `save_contacts_and_pictures.sh` – helper to seed device test data (contacts, images)
* `ResultCollector.py` – aggregates run outputs for CI/archiving

> Check the script headers for usage. Most scripts accept env vars and print usage with `-h`.

---

## Local Emulator Tips

* Use the provided `avd_config*.ini` as a reference when creating AVDs
* Make sure `adb devices` shows your emulator/phone
* Start Appium with the proper driver (e.g., `uiautomator2`) and check the logs for capabilities picked up from env

---

## Coding Conventions

* Page Objects & screens live under `core/` (example: `core/pages/`)
* Shared fixtures go to `tests/conftest.py`
* Test naming: `test_*` modules & functions
* Keep tests **idempotent** and **data‑independent** where possible

---

## Troubleshooting

* **Session creation fails** → Verify `APPIUM_SERVER_URL` and that the driver is installed (`appium driver list --installed`)
* **APK not found** → Ensure `APP_PATH` is an absolute path accessible inside Docker/CI
* **Element not found** → Add proper waits (explicit waits in core helpers)
* **Emulator slow** → Disable animations, use x86\_64 images with hardware accel

---

## Security & Secrets

* Do **not** commit real credentials, API keys or internal URLs
* Use environment variables and masked CI variables
* Keep `requirements.txt` pinned and upgrade periodically

---
## Maintainer

* @bikmax (Max) – automation engineer / maintainer

---

