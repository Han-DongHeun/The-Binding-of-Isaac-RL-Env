import re
import yaml
import subprocess
import sys

# --- 설정 ---
TARGET_PYTHON_VERSION = "3.13.2"

# PyTorch 관련 설정 (필요에 따라 수정)
PYTORCH_VERSION = "2.6.0+cu126"
TORCHVISION_VERSION = "0.21.0+cu126"
TORCHAUDIO_VERSION = "2.6.0+cu126"
PYTORCH_INDEX_URL = "https://download.pytorch.org/whl/cu126"
# ----------------

def remove_ansi_escape(text):
    """ANSI 이스케이프 시퀀스를 제거합니다."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def get_conda_history_deps():
    """'conda env export --from-history'를 실행하여 기본 의존성을 가져옵니다."""
    try:
        conda_env_proc = subprocess.run(
            ["conda", "env", "export", "--from-history", "--no-builds"],
            capture_output=True, text=True, check=True, encoding='utf-8'
        )
        clean_output = remove_ansi_escape(conda_env_proc.stdout)
        env_data = yaml.safe_load(clean_output)
        # prefix 키 제거
        env_data.pop("prefix", None)
        return env_data
    except subprocess.CalledProcessError as e:
        print(f"Error running conda env export: {e}", file=sys.stderr)
        print(f"Stderr: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing conda env export output: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


def get_pip_freeze_packages():
    """'pip freeze'를 실행하여 설치된 pip 패키지 목록을 가져옵니다."""
    try:
        pip_freeze_proc = subprocess.run(
            ["pip", "freeze"], capture_output=True, text=True, check=True, encoding='utf-8'
        )
        pip_lines = pip_freeze_proc.stdout.strip().splitlines()
        # VCS 설치 (@) 제외, 빈 줄 제외
        pip_packages = [line.strip() for line in pip_lines if line.strip() and "@" not in line]
        return pip_packages
    except subprocess.CalledProcessError as e:
        print(f"Error running pip freeze: {e}", file=sys.stderr)
        print(f"Stderr: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred during pip freeze: {e}", file=sys.stderr)
        sys.exit(1)

# 1. Conda 기록 기반 의존성 가져오기
print("1. Fetching Conda dependencies from history...")
env_data = get_conda_history_deps()

# 2. Python 버전 설정 (호환성 확인!)
print(f"2. Setting Python version to {TARGET_PYTHON_VERSION}...")
conda_deps = env_data.get("dependencies", [])
python_found = False
updated_conda_deps = []
for i, dep in enumerate(conda_deps):
    if isinstance(dep, str) and dep.startswith("python"):
        updated_conda_deps.append(f"python={TARGET_PYTHON_VERSION}")
        python_found = True
    # pip 관련 딕셔너리는 일단 제외 (나중에 재구성)
    elif isinstance(dep, dict) and "pip" in dep:
        continue # Skip existing pip dict, will rebuild later
    else:
        updated_conda_deps.append(dep)

if not python_found:
    updated_conda_deps.insert(0, f"python={TARGET_PYTHON_VERSION}") # 맨 앞에 추가

env_data["dependencies"] = updated_conda_deps

# 3. Conda 의존성 이름 추출 (pip 목록 필터링용)
conda_dep_names = set()
for dep in env_data.get("dependencies", []):
    if isinstance(dep, str):
        # 'package>=version', 'package=version', 'package' 등을 처리
        match = re.match(r"^[a-zA-Z0-9_-]+", dep)
        if match:
            conda_dep_names.add(match.group(0))
print(f"   Found Conda managed packages: {conda_dep_names}")

# 4. pip freeze 목록 가져오기
print("4. Fetching pip freeze list...")
pip_freeze_list = get_pip_freeze_packages()

# 5. pip 패키지 목록 재구성
print("5. Reconstructing pip package list...")
final_pip_packages = []

# PyTorch 패키지 정의 (사용자 설정 기반)
torch_packages_to_add = [
    f"--index-url {PYTORCH_INDEX_URL}",
    f"torch=={PYTORCH_VERSION}",
    f"torchvision=={TORCHVISION_VERSION}",
    f"torchaudio=={TORCHAUDIO_VERSION}"
]

# pip freeze 목록에서 Conda가 관리하지 않고, PyTorch 관련도 아닌 패키지 필터링
for pkg_line in pip_freeze_list:
    # 'package==version' 에서 'package' 부분 추출
    pkg_name_match = re.match(r"^[a-zA-Z0-9_-]+", pkg_line)
    if pkg_name_match:
        pkg_name = pkg_name_match.group(0).lower().replace('_', '-') # 표준화

        if pkg_name not in conda_dep_names and not pkg_name.startswith(("torch", "torchvision", "torchaudio")):
            final_pip_packages.append(pkg_line)


# 정의된 PyTorch 패키지 추가
final_pip_packages.extend(torch_packages_to_add)
print(f"   Final pip list includes: {final_pip_packages}")


# 6. 최종 environment.yml 구조 생성
print("6. Building final environment.yml structure...")
final_dependencies = []
pip_dict_added = False

# 기존 Conda 의존성 추가
for dep in env_data.get("dependencies", []):
    # 문자열 의존성만 추가 (이미 위에서 python 버전 수정됨)
    if isinstance(dep, str):
        final_dependencies.append(dep)

# 'pip' 자체가 Conda 의존성에 없으면 추가
if "pip" not in conda_dep_names:
    final_dependencies.append("pip")

# 재구성된 pip 패키지 목록 추가 (목록이 비어있지 않다면)
if final_pip_packages:
    final_dependencies.append({"pip": final_pip_packages})

env_data["dependencies"] = final_dependencies

# 7. environment.yml 파일 저장
print("7. Saving environment.yml...")
try:
    with open("environment.yml", "w", encoding='utf-8') as f:
        yaml.dump(env_data, f, sort_keys=False, default_flow_style=False)
    print("✅ environment.yml 생성 완료!")

except Exception as e:
    print(f"Error writing environment.yml file: {e}", file=sys.stderr)
    sys.exit(1)