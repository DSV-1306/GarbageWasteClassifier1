import { useState } from "react";
import { ImageUpload } from "@/components/ImageUpload";
import { ClassificationResult, WasteCategory } from "@/components/ClassificationResult";
import { Button } from "@/components/ui/button";
import { Loader2 } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

const Index = () => {
  const [preview, setPreview] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  // ✅ waste category is strongly typed
  const [category, setCategory] = useState<WasteCategory | null>(null);
  const [confidence, setConfidence] = useState<number | null>(null);

  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const { toast } = useToast();

  const handleImageSelect = (file: File, previewUrl: string) => {
    setSelectedFile(file);
    setPreview(previewUrl);
    setCategory(null);
    setConfidence(null);
  };

  const handleClear = () => {
    setPreview(null);
    setSelectedFile(null);
    setCategory(null);
    setConfidence(null);
  };

  const analyzeImage = async () => {
    if (!selectedFile) return;
    setIsAnalyzing(true);

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      // ✅ FIX: safely cast backend string to WasteCategory type
      setCategory(data.prediction as WasteCategory);
      setConfidence(data.confidence);

      toast({
        title: "✅ Classification Complete",
        description: `Result: ${data.prediction} (${data.confidence}%)`,
      });

    } catch (error) {
      toast({
        title: "❌ Backend Error",
        description: "Backend not running. Start FastAPI server.",
        variant: "destructive",
      });
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center text-center bg-[#020202] text-white">
      <h1 className="text-4xl font-bold text-green-500 drop-shadow-xl">
        AI Garbage Waste Classifier
      </h1>
      <p className="mt-2 mb-6 text-gray-300">
        Upload waste image and get prediction & confidence
      </p>

      <div className="w-full max-w-xl">
        <ImageUpload preview={preview} onSelect={handleImageSelect} onClear={handleClear} />
      </div>

      {selectedFile && (
        <Button
          className="mt-6 w-48 h-12 text-lg bg-green-600 hover:bg-green-700"
          onClick={analyzeImage}
        >
          {isAnalyzing ? <Loader2 className="animate-spin" /> : "Classify Waste"}
        </Button>
      )}

      {category && (
        <ClassificationResult category={category} confidence={confidence ?? undefined} />
      )}
    </div>
  );
};

export default Index;
