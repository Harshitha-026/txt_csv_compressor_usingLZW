# import streamlit as st
# import os 
# import tempfile
# from lzw_compress import compress
# from lzw_decompress import decompress

# st.set_page_config(page_title="LZW Compression Tool",  layout="centered")

# st.title("LZW File Compression & Decompression")
# st.write("Upload any file (CSV, TXT) to compress or decompress using the LZW algorithm.")

# # Sidebar for mode selection
# st.sidebar.header("Select Operation")
# action = st.sidebar.radio("Choose an option:", ["Compress File", "Decompress File"])

# # Temporary directory for file handling
# temp_dir = tempfile.mkdtemp()

# #COMPRESSION
# if action == "Compress File":
#     st.header("🗜️ Compress a File")

#     uploaded_file = st.file_uploader("Upload a file to compress", type=None)

#     if uploaded_file is not None:
#         input_path = os.path.join(temp_dir, uploaded_file.name)
#         with open(input_path, "wb") as f:
#             f.write(uploaded_file.read())

#         st.success(f"File uploaded: {uploaded_file.name}")

#         if st.button("Compress Now"):
#             output_file = os.path.splitext(uploaded_file.name)[0] + ".lzw"
#             output_path = os.path.join(temp_dir, output_file)

#             compress(input_path, output_path)

#             # Calculate sizes and ratio
#             original_size = os.path.getsize(input_path)
#             compressed_size = os.path.getsize(output_path)
#             ratio = ((original_size - compressed_size) / original_size) * 100

#             st.subheader("Compression Summary")
#             st.write(f"Original size: {original_size / 1024:.2f} KB")
#             st.write(f"Compressed size: {compressed_size / 1024:.2f} KB")

#             if ratio >= 0:
#                 st.success(f"Compression Ratio: {ratio:.2f}% smaller")
#             else:
#                 st.warning(f"Compression Ratio: {abs(ratio):.2f}% larger (file expanded slightly)")

#             st.download_button(
#                 label="Download Compressed File",
#                 data=open(output_path, "rb").read(),
#                 file_name=output_file,
#                 mime="application/octet-stream"
#             )

# #DECOMPRESSION
# elif action == "Decompress File":
#     st.header("Decompress a File")

#     uploaded_file = st.file_uploader("Upload a .lzw file to decompress", type=["lzw"])

#     if uploaded_file is not None:
#         input_path = os.path.join(temp_dir, uploaded_file.name)
#         with open(input_path, "wb") as f:
#             f.write(uploaded_file.read())

#         st.success(f"File uploaded: {uploaded_file.name}")

#         if st.button("Decompress Now"):
#             output_path = decompress(input_path)

#             # Calculate decompressed file size
#             decompressed_size = os.path.getsize(output_path)
#             compressed_size = os.path.getsize(input_path)

#             st.subheader("Decompression Summary")
#             st.write(f"**Compressed size:** {compressed_size / 1024:.2f} KB")
#             st.write(f"**Decompressed size:** {decompressed_size / 1024:.2f} KB")

#             st.download_button(
#                 label="Download Decompressed File",
#                 data=open(output_path, "rb").read(),
#                 file_name=os.path.basename(output_path),
#                 mime="application/octet-stream"
#             )



import os
import streamlit as st
from lzw_compress import compress
from lzw_decompress import decompress

def main():
    st.title("LZW Compression & Decompression Tool")
    st.write("Efficient file compression and decompression using the Lempel–Ziv–Welch (LZW) algorithm.")

    mode = st.radio("Select Operation:", ("Compress a File", "Decompress a File"))

    if mode == "Compress a File":
        uploaded_file = st.file_uploader("Upload a file to compress", type=None)
        if uploaded_file is not None:
            input_path = f"temp_{uploaded_file.name}"
            with open(input_path, "wb") as f:
                f.write(uploaded_file.read())

            if st.button("Compress"):
                output_file, original_size, compressed_size, duration = compress(input_path)

                st.success("File compressed successfully!")
                st.write(f"Original Size: {original_size / 1024:.2f} KB")
                st.write(f"Compressed Size: {compressed_size / 1024:.2f} KB")
                st.write(f"Compression Ratio: {(original_size/compressed_size ):.2f}")
                st.write(f"Compression percentage: {(1-(compressed_size/original_size) ) * 100:.2f}%")                
                st.write(f"Time Taken: {duration:.3f} seconds")

                with open(output_file, "rb") as f:
                    st.download_button(
                        label= "Download Compressed File",
                        data=f,
                        file_name=os.path.basename(output_file),
                        mime="application/octet-stream"
                    )

    elif mode == "Decompress a File":
        uploaded_file = st.file_uploader("Upload a .lzw file to decompress", type=["lzw"])
        if uploaded_file is not None:
            input_path = f"temp_{uploaded_file.name}"
            with open(input_path, "wb") as f:
                f.write(uploaded_file.read())

            if st.button("Decompress"):
                try:
                    output_file, decompressed_size, duration = decompress(input_path)

                    st.success("File decompressed successfully!")
                    st.write(f"Decompressed Size: {decompressed_size / 1024:.2f} KB")
                    st.write(f"Time Taken: {duration:.3f} seconds")

                    with open(output_file, "rb") as f:
                        st.download_button(
                            label="Download Decompressed File",
                            data=f,
                            file_name=os.path.basename(output_file),
                            mime="application/octet-stream"
                        )
                except Exception as e:
                    st.error(f"Decompression failed: {e}")

if __name__ == "__main__":
    main()
