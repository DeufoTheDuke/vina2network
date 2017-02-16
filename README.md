# vina2network

Vina2Network is a python script that aims to automate and distribute Molecular Docking using the Autodock Vina platform, thus allowing for a Virtual Screening methodology with Vina. This distribution is done by using computers connected to the network and running this script to process the docking. The script uses python FTP functionalities for network distribution. PyFTPdlib (https://github.com/giampaolo/pyftpdlib) was used.

The script is divided into 2 modes: Server and Client. The Server is where the input files (Ligand, Receptors) are stored, and where the user will input the Autodock Vina docking paramenters. Each client computer then receives the receptor and parameters file, and get a ligand from the computer acting as server. Then the computer attempts to dock this ligand to the receptor using the parameters the user stipulated. If no errors occurred, the Client sends the results back to the Server, and gets another Ligand.

### Requirements


**Operating System:** Linux (eg: Ubuntu) 32/64-bits

**Python Libraries:** PyFTPdlib

**Third-Party Programs:** Autodock Vina

### Usage

**Vina2Network exclusive Commands**

**'--ligand_dir'** **:**	Ligand directory (PDBQT file)
**'--mode'** **:**	Client or server mode
**'--host_ip'** **:**	The server computer IP
**'--host_port'** **:**	The server computer Port

**Autodock Vina Commands**

**'--receptor'** **:**	Receptor file (PDBQT file)
**'--flex'** **:**  Receptor flexible side chain (if it's used)
**'--center_x'** **:**	X side Grid Box Coordinate
**'--center_y'** **:**	Y side Grid Box Coordinate
**'--center_z'** **:**	Z side Grid Box Coordinate
**'--size_x'** **:**	X side Grid Box Size
**'--size_y'** **:**	Y side Grid Box Size
**'--size_z'** **:**	Z side Grid Box Size
**'--help'** **:**	Show the script commands
**'--log'** **:**	Creates a log file
**'--cpu'** **:**	Number of cores (per CPU)
**'--seed'** **:**	Changes the random seed
**'--exhaustiveness'** **:**	Exhaustiveness of the search
**'--num_modes'** **:**	Number of binding modes generated
**'--energy_range'** **:**	Max energy difference between best and worst binding

### Contact

If you have any question or feedback, contact me:

Rafael Woloski // rafael.woloski@ufpel.edu.br
