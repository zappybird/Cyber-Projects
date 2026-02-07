# Security Policy

## 1. Purpose

This project is an **educational cybersecurity demonstration** intended for learning, debugging, and defensive research.  
It is **not** designed, intended, or supported for malicious use, covert monitoring, or unauthorized data collection.

The codebase intentionally avoids features associated with malware, such as stealth execution, persistence, remote exfiltration, or covert installation.

---

## 2. Supported Use Cases

The project may be used for:

- Personal cybersecurity education  
- Understanding keystroke logging mechanics  
- Debugging keyboard input behavior  
- Defensive research and detection practice  
- Academic or lab environments where all participants consent  

Any use outside these boundaries is **not supported**.

---

## 3. Prohibited Use Cases

The following activities are strictly prohibited:

- Monitoring another person’s device without explicit consent  
- Deploying the software covertly or without user awareness  
- Adding persistence, stealth, or remote communication features  
- Using the project for surveillance, credential theft, or unauthorized access  
- Incorporating the code into malware or malicious tooling  

If you are unsure whether your use case is appropriate, assume it is **not allowed**.

---

## 4. Security Design Principles

This project is intentionally built with safeguards to prevent misuse:

### **No Stealth Behavior**
- Visible console output  
- Manual execution required  
- No background services  
- No obfuscation  

### **No Persistence**
- Does not install itself  
- Does not modify system settings  
- Does not run on startup  

### **No Remote Exfiltration**
- No networking code  
- No HTTP requests, sockets, or uploads  
- All logs remain local  

### **User-Controlled Shutdown**
- ESC key immediately stops the logger  
- Final word is flushed on exit  

### **Transparent Codebase**
- Readable, documented Python  
- Public CHANGELOG  
- Clear ethical warnings  

These design choices ensure the project remains a **learning tool**, not a covert threat.

---

## 5. Reporting Security Concerns

If you discover a vulnerability, misuse pattern, or potential improvement related to safety or ethical safeguards, please open an issue on GitHub with the label:


Do **not** report malicious use of the code — instead, contact the appropriate authorities or platform administrators.

---

## 6. Disclaimer

This project is provided **as-is**, without warranty or liability.  
The author is **not responsible** for misuse, modification, or illegal deployment of the code.

Users are solely responsible for ensuring their use complies with all applicable laws and ethical standards.

---

## 7. Responsible Use

By using this project, you agree to:

- Operate it only on systems you own or have explicit permission to test  
- Respect privacy and legal boundaries  
- Use the code for learning, research, or defensive purposes only  

If these conditions cannot be met, you must not use this software.
