import re

def get_ip_addresses(count):
    """Ask the user to input new IP addresses."""
    new_ips = []
    for i in range(1, count + 1):
        new_ip = input(f"Enter new IP address for newIp{i}: ")
        new_ips.append(new_ip)
    return new_ips

def replace_ips_in_file(file_path, old_ips, new_ips):
    """Find and replace IPs in the specified file."""
    with open(file_path, 'r') as file:
        content = file.read()

    for old_ip, new_ip in zip(old_ips, new_ips):
        content = re.sub(re.escape(old_ip), new_ip, content)

    with open(file_path, 'w') as file:
        file.write(content)

def extract_current_ips(file_path, alias_prefix):
    """Extract current IPs associated with the aliases from the file."""
    aliases = [f"{alias_prefix}{i}" for i in range(1, 4)]
    old_ips = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

    for alias in aliases:
        for line in lines:
            if alias in line:
                match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                if match:
                    old_ips.append(match.group(1))
                    break

    return old_ips

def main():
    bashrc_path = "~/.bashrc"
    inventory_path = "./inventory"

    # Ask user how many IPs they'd like to update
    ip_count = int(input("How many IP addresses would you like to enter (up to 3)? "))
    if ip_count > 3:
        print("Maximum allowed IP count is 3.")
        return

    # Get new IP addresses
    new_ips = get_ip_addresses(ip_count)

    # Extract current IPs from .bashrc
    bashrc_path = bashrc_path.replace("~", "./")  # Adjust for file path handling
    old_ips = extract_current_ips(bashrc_path, "vmlogin")

    if len(old_ips) < ip_count:
        print("Not enough existing aliases found in .bashrc.")
        return

    # Replace IPs in .bashrc
    print("Updating .bashrc...")
    replace_ips_in_file(bashrc_path, old_ips[:ip_count], new_ips)

    # Replace IPs in inventory
    print("Updating inventory...")
    replace_ips_in_file(inventory_path, old_ips[:ip_count], new_ips)

    print("Update complete.")

if __name__ == "__main__":
    main()

