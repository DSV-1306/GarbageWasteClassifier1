// ✅ Type definition used everywhere
export type WasteCategory = "organic" | "recyclable" | "e-waste";

interface Props {
  category: WasteCategory;
  confidence?: number;
}

export const ClassificationResult = ({ category, confidence }: Props) => {
  const color =
    category === "organic"
      ? "text-green-400"
      : category === "recyclable"
      ? "text-blue-400"
      : "text-yellow-400";

  return (
    <div className="mt-6 p-4 bg-gray-800/50 rounded-xl shadow-lg">
      <h2 className={`text-3xl font-bold ${color}`}>{category.toUpperCase()}</h2>

      {confidence !== undefined && (
        <p className="mt-2 text-gray-300 text-lg">
          Confidence: <span className="font-semibold">{confidence}%</span>
        </p>
      )}
    </div>
  );
};
