import argparse
import subprocess
import re
import os
import sys

def bump_version(workspace_root):
    vbproj_path = os.path.join(workspace_root, "CirculatingBox", "CirculatingBox.vbproj")
    pubxml_path = os.path.join(workspace_root, "CirculatingBox", "Properties", "PublishProfiles", "ClickOnceProfile.pubxml")
    
    if not os.path.exists(vbproj_path):
        print(f"Error: Could not find {vbproj_path}")
        sys.exit(1)
        
    with open(vbproj_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    def bump_match(m):
        parts = m.group(1).split('.')
        parts[-1] = str(int(parts[-1]) + 1)
        new_ver = '.'.join(parts)
        tag_name = m.group(0).split('>')[0][1:]
        print(f"Bumped {tag_name} to {new_ver}")
        return f"<{tag_name}>{new_ver}</{tag_name}>"

    content = re.sub(r'<AssemblyVersion>(.*?)</AssemblyVersion>', bump_match, content)
    content = re.sub(r'<FileVersion>(.*?)</FileVersion>', bump_match, content)
    
    with open(vbproj_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    if not os.path.exists(pubxml_path):
        print(f"Error: Could not find {pubxml_path}")
        sys.exit(1)
        
    with open(pubxml_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    def bump_rev(m):
        rev = int(m.group(1)) + 1
        print(f"Bumped ApplicationRevision to {rev}")
        return f"<ApplicationRevision>{rev}</ApplicationRevision>"
        
    content = re.sub(r'<ApplicationRevision>(\d+)</ApplicationRevision>', bump_rev, content)
    
    with open(pubxml_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Success! Versions bumped. Project paths updated in {workspace_root}")

def deploy(workspace_root):
    deploy_script = os.path.join(workspace_root, "CirculatingBox", "DEPLOY_TO_SERVER.cmd")
    if not os.path.exists(deploy_script):
         print(f"Error: Could not find {deploy_script}")
         sys.exit(1)
         
    vswhere_cmd = r'"C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe" -latest -property installationPath'
    try:
        vs_path = subprocess.check_output(vswhere_cmd, shell=True, text=True).strip()
    except subprocess.CalledProcessError:
        print("Error: Could not locate Visual Studio installation via vswhere.exe")
        sys.exit(1)
        
    vs_dev_cmd = os.path.join(vs_path, "Common7", "Tools", "VsDevCmd.bat")
    
    cmd = f'cmd.exe /c ""{vs_dev_cmd}" && (echo. | "{deploy_script}")"'
    
    print(f"Executing: {cmd}")
    process = subprocess.Popen(cmd, shell=True, cwd=os.path.join(workspace_root, "CirculatingBox"), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
    
    for line in process.stdout:
        sys.stdout.buffer.write(line.encode("utf-8", errors="replace"))
        sys.stdout.flush()
        
    process.wait()
    if process.returncode != 0:
        print(f"Deployment failed with exit code {process.returncode}")
        sys.exit(process.returncode)
    else:
        print("Deployment completed successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CirculatingBox Publisher Script")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    bump_parser = subparsers.add_parser("bump")
    bump_parser.add_argument("--workspace", required=True, help="Path to CirculatingBox workspace root")
    
    deploy_parser = subparsers.add_parser("deploy")
    deploy_parser.add_argument("--workspace", required=True, help="Path to CirculatingBox workspace root")
    
    args = parser.parse_args()
    
    if args.command == "bump":
        bump_version(args.workspace)
    elif args.command == "deploy":
        deploy(args.workspace)
