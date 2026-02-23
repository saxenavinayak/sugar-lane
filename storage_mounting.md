## Mounting a new HDD
Helpful guide: https://help.ubuntu.com/community/InstallingANewHardDrive

#### Quickstart
1. Grab the newly installed HDD's logical name, doing (should be able to see by size)
`sudo lshw -C disk`

2. Also grab UUID of new HDD
`sudo blkid`

3. Partition the hard drives (ie., logical separations based on how you want to divide data: videos, logs, etc.) -> Can use GPT or MBR partitions, use GPT as MBR has maxPartition of 4 and maxParitionSize of 2tb

4. Use parted for partitions
`sudo parted /dev/sdb`
`mklabel gpt`
`unit TB`
`mkpart`
        primary, ext4,  0, 4 
(4  for a 4tb hard drive)


5. Format new partition as ext4, `sudo mkfs -t extr /dev/sdb1`

6. Make new directory where hard drive will be mounted: `sudo mkdir /media/chungus`
7. Mount hard drive, OS will auto do it if you edit /etc/fstab
Add this line: `/dev/disk/by-uuid/f62ad702-06cd-4969-a3f0-f6ddb0e92ea0 /media/chungus ext4 defaults 0 2`