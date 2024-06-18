import netaddr
from netaddr import spanning_cidr


def read_ip_list(filepath):
    with open(filepath, 'r') as file:
        lines = [line.strip() for line in file if line.strip() and '-' in line and '.' in line]
    print(f"Read {len(lines)} lines from {filepath} after filtering IPv6")
    return lines


def range_to_cidr(range):
    start_ip, end_ip = range.split('-')
    try:
        return spanning_cidr([start_ip, end_ip])
    except:
        # Skip IPv6 ranges
        return []


def merge_cidr_blocks(cidr_blocks):
    merged = netaddr.cidr_merge(cidr_blocks)
    print(f"Merged {len(cidr_blocks)} CIDR blocks into {len(merged)}")
    return merged


raw_ip_list = read_ip_list('tmp/VN-suip.biz.txt')
cidr_list = []
for ip_range in raw_ip_list:
    cidr_list.append(range_to_cidr(ip_range))
merged_cidr = merge_cidr_blocks(cidr_list)
with open('out/vn_ipv4_cidr.txt', 'w') as file:
    for cidr in merged_cidr:
        file.write(str(cidr) + '\n')
