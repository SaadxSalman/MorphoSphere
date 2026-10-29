import py_compile
import os

base = 'backend/app'
files = []
for root, dirs, fs in os.walk(base):
    for f in fs:
        if f.endswith('.py'):
            files.append(os.path.join(root, f))

for f in sorted(files):
    try:
        py_compile.compile(f, doraise=True)
        print(f'OK: {f}')
    except py_compile.PyCompileError as e:
        print(f'FAIL: {f} - {e}')

print(f'\nChecked {len(files)} Python files')