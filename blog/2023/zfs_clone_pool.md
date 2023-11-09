---
blogpost: true
date: Nov 09, 2023
author: Jens W. Klein
location: Austria
category: Linux
language: en
---

# Clone ZFS Pool To New Disk for replacement

Plan: Replace old ZFS formatted NVMe SSD with new, larger one.

My Tuxedo Infinity-Book has two M2-slots, at different speeds.
1st an older Samsung 970 EVO Plus 2TB Gen3 and 2nd a fast Samsung 980 PRO 512GB.
Latter should be replaced as it fills up recently.

I put the new Samsung 980 PRO 1TB in an USB external case and connected it to the notebook.

To copy the data, I first created a snapshot of my existing pool - all as root:

`zfs snapshot -r speedy@migrate`

Then I created a new pool on the new SSD with a new name:

`zpool create speedy2 /dev/sdb`

Then I send the snapshot to the new pool:

`zfs send -R speedy@migrate | zfs receive -F speedy2`

Go for a coffee - it takes a while.
Now with fresh caffein in the blood stream, I removed the old pool:

`zpool export speedy`

Finally I shutdown the computer, opened the bottom, exchanged SSD, booted again and then imported the new pool with the name of the old one - in fact a rename:

`zpool import speedy2 speedy`

Done.