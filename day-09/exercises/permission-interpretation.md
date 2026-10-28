# Day 9 - Permission Interpretation Exercise

## 1. Permission String: `-rw-------`
* **File Type:** Regular file (`-`)
* **Owner (`rw-`):** Can read and write/modify the file.
* **Group (`---`):** Has no permissions at all.
* **Others (`---`):** Has no permissions at all.
* **Practical Meaning:** A strictly private file (like an SSH private key) accessible only by the owner.

## 2. Permission String: `-rw-r--r--`
* **File Type:** Regular file (`-`)
* **Owner (`rw-`):** Can read and write/modify the file.
* **Group (`r--`):** Can only read the file; cannot modify it.
* **Others (`r--`):** Can only read the file; cannot modify it.
* **Practical Meaning:** A public read-only text file or document where only the owner has editing rights.

## 3. Permission String: `-rwxr-x---`
* **File Type:** Regular file (`-`)
* **Owner (`rwx`):** Has full control (read, write, and execute/run).
* **Group (`r-x`):** Can read and execute/run the file, but cannot modify it.
* **Others (`---`):** Has no permissions at all.
* **Practical Meaning:** An application script or utility where trusted group members can execute the program, but outsiders are blocked.

## 4. Permission String: `drwx------`
* **File Type:** Directory (`d`)
* **Owner (`rwx`):** Can list contents (`r`), add/delete files (`w`), and traverse/enter (`x`).
* **Group (`---`):** Has no access.
* **Others (`---`):** Has no access.
* **Practical Meaning:** A secure private directory (such as a user home folder) hidden from all other system users.
