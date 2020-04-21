
import subprocess
chrome_path = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
p = subprocess.Popen([chrome_path, r'file://C:\Users\HimanshuKholiya\Desktop\okta2\Resume\AmanPAnt.pdf']) #This uses 'Subprocess' to open the file
returncode = p.wait() 