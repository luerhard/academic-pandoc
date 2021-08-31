from pathlib import Path
import re
import sys

def main():
    
    path = Path(sys.argv[1])
    text = path.read_text()
    text = re.sub(r"\\leavevmode\\vadjust pre{(.*?)}{}}", r"\g<1>}{}", text)
    path.write_text(text)
    
    
if __name__ == "__main__":
    main()
    
    
