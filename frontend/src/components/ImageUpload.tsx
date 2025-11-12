import React from "react";

interface ImageUploadProps {
  preview?: string | null;
  onSelect: (file: File, previewUrl: string) => void;
  onClear: () => void;
}

export const ImageUpload = ({ preview, onSelect, onClear }: ImageUploadProps) => {

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const previewUrl = URL.createObjectURL(file);
    onSelect(file, previewUrl);
  };

  return (
    <div className="w-full flex flex-col items-center justify-center border border-green-500 rounded-2xl p-6 bg-black/20 backdrop-blur-xl">
      {!preview ? (
        <label className="cursor-pointer flex flex-col items-center justify-center text-gray-300">
          Click to upload image
          <input type="file" hidden accept="image/*" onChange={handleFileChange} />
        </label>
      ) : (
        <>
          <img src={preview} className="max-h-80 rounded-xl" />
          <button className="mt-4 px-4 py-2 bg-red-600 rounded-xl text-white" onClick={onClear}>
            Remove Image
          </button>
        </>
      )}
    </div>
  );
};

export default ImageUpload;
