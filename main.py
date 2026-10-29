"""
========================================================================================
Project Name: Browser & App Artifact Timeline Visualizer ("TraceLens")
Academic Level: First Year Computer Science & Engineering Project
Academic Year: 2026-2027

Group Members & Contributions:
1. Tanishq Gunjal   (PRN: 1272261851 | 1272261851.t@mitwpu.edu.in) - Project Lead & GUI
2. Janhavi Dahiwale (PRN: 1272261225 | 1272261225.j@mitwpu.edu.in) - Browser Forensics Parser
3. OM Nalawade      (PRN: 1272261153 | 1272261153.o@mitwpu.edu.in) - OS Artifacts & Timeline Engine
4. Ayush Warudkar   (PRN: 1272261894 | 1272261894.a@mitwpu.edu.in) - Visual Analytics & Reports
========================================================================================
"""

import sys
import os

# Add project root directory to Python module search path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from gui.app_window import TraceLensApp


def print_banner():
    """
    Displays the project banner and group member credentials in console.
    """
    banner = r"""
================================================================================
   ______                  __                     
  /_  __/________ ________/ /   ___  ____  _____   
   / / / ___/ __ `/ ___/ _  /   / _ \/ __ \/ ___/   
  / / / /  / /_/ / /__/  __/   /  __/ / / (__  )    
 /_/ /_/   \__,_/\___/\___/   \___/_/ /_/____/     
                                                   
 TraceLens - Browser & App Artifact Timeline Visualizer
 First Year Engineering Group Project Submission (2026-2027)
================================================================================
 Project Group Members:
   1. Tanishq Gunjal   - Lead / GUI Architecture & Integration
   2. Janhavi Dahiwale - Browser Forensics Parser (Chrome & Edge)
   3. OM Nalawade      - Windows App Artifacts & Correlation Engine
   4. Ayush Warudkar   - Visual Analytics & Reporting Engine
================================================================================
 Starting GUI application...
"""
    print(banner)


def main():
    """
    Application main function.
    """
    print_banner()
    app = TraceLensApp()
    app.mainloop()


if __name__ == "__main__":
    main()
