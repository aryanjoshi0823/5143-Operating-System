def split_binary_file_to_chunks(file_path, chunk_size=1024):
    chunks = []

    with open(file_path, "rb") as file:
        while True:
            # Read a chunk of size `chunk_size`
            chunk = file.read(chunk_size)
            if not chunk:
                break  # End of file
            chunks.append(chunk)

    return chunks


def split_file_to_chunks(file_path, chunk_size=1024, encoding="utf-8"):
    chunks = []

    with open(file_path, "r", encoding=encoding) as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break  # End of file
            chunks.append(chunk)

    return chunks