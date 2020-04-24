from util import remote_fn


@remote_fn
def scrub(volume_id):
    import time
    import rawfile_util

    rawfile_util.patch_metadata(volume_id, {"deleted_at": time.time()})


@remote_fn
def init_rawfile(volume_id, size):
    import time
    import rawfile_util
    from util import run

    img_dir = rawfile_util.img_dir(volume_id)
    img_dir.mkdir(parents=False, exist_ok=False)
    img_file = f"{img_dir}/disk.img"
    rawfile_util.patch_metadata(
        volume_id,
        {
            "volume_id": volume_id,
            "created_at": time.time(),
            "img_file": img_file,
            "size": size,
        },
    )
    run(f"truncate -s {size} {img_file}")
    run(f"mkfs.ext4 {img_file}")