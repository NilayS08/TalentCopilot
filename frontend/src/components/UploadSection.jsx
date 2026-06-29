import { useState, useRef } from "react";
import { BsCloudUpload, BsCheckCircle, BsXCircle, BsFiletypePdf } from "react-icons/bs";

export default function UploadSection({ onJDUpload, onResumeUpload, onEvaluate, jdUploaded, resumeCount, evaluating }) {
  const [jdFile, setJdFile] = useState(null);
  const [resumeFiles, setResumeFiles] = useState([]);
  const [jdUploading, setJdUploading] = useState(false);
  const [resumeUploading, setResumeUploading] = useState(false);
  const jdRef = useRef(null);
  const resumeRef = useRef(null);

  const handleJDFile = async (file) => {
    if (!file) return;
    setJdFile(file);
    setJdUploading(true);
    try {
      await onJDUpload(file);
    } catch (e) {
      setJdFile(null);
    } finally {
      setJdUploading(false);
    }
  };

  const handleResumeFiles = async (files) => {
    if (!files.length) return;
    setResumeFiles((prev) => [...prev, ...files]);
    setResumeUploading(true);
    try {
      await onResumeUpload(files);
    } catch (e) {
      // remove failed files from display
    } finally {
      setResumeUploading(false);
    }
  };

  const removeResume = (idx) => {
    setResumeFiles((prev) => prev.filter((_, i) => i !== idx));
  };

  const displayFiles = resumeFiles.slice(0, 3);
  const extraCount = resumeFiles.length - 3;

  return (
    <div className="mb-8">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-6">
          <h3 className="text-sm font-semibold text-gray-700 mb-4">1. Upload Job Description</h3>
          {!jdFile ? (
            <div
              onDragOver={(e) => e.preventDefault()}
              onDrop={(e) => { e.preventDefault(); handleJDFile(e.dataTransfer.files[0]); }}
              className="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center cursor-pointer hover:border-blue-400 transition-colors"
              onClick={() => jdRef.current?.click()}
            >
              <BsCloudUpload className="mx-auto text-3xl text-gray-400 mb-3" />
              <p className="text-sm text-gray-500 mb-2">Drag & Drop JD here</p>
              <p className="text-xs text-gray-400">or</p>
              <span className="inline-block mt-2 text-sm text-blue-600 font-medium hover:underline">Browse File</span>
              <input ref={jdRef} type="file" accept=".pdf" className="hidden" onChange={(e) => handleJDFile(e.target.files[0])} />
            </div>
          ) : (
            <div className="flex items-center gap-3 p-4 bg-green-50 rounded-xl border border-green-200">
              <BsCheckCircle className="text-green-600 text-lg shrink-0" />
              <span className="text-sm text-green-800 truncate flex-1">{jdFile.name}</span>
              <button
                onClick={() => { setJdFile(null); }}
                className="text-gray-400 hover:text-red-500"
              >
                <BsXCircle />
              </button>
            </div>
          )}
          {jdUploading && <p className="text-xs text-blue-600 mt-2">Uploading JD...</p>}
        </div>

        <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-6">
          <h3 className="text-sm font-semibold text-gray-700 mb-4">2. Upload Resumes</h3>
          {resumeFiles.length === 0 ? (
            <div
              onDragOver={(e) => e.preventDefault()}
              onDrop={(e) => { e.preventDefault(); handleResumeFiles(Array.from(e.dataTransfer.files)); }}
              className="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center cursor-pointer hover:border-blue-400 transition-colors"
              onClick={() => resumeRef.current?.click()}
            >
              <BsCloudUpload className="mx-auto text-3xl text-gray-400 mb-3" />
              <p className="text-sm text-gray-500 mb-2">Drag & Drop Resumes here</p>
              <p className="text-xs text-gray-400">or</p>
              <span className="inline-block mt-2 text-sm text-blue-600 font-medium hover:underline">Browse Files</span>
              <input ref={resumeRef} type="file" accept=".pdf" multiple className="hidden" onChange={(e) => handleResumeFiles(Array.from(e.target.files))} />
            </div>
          ) : (
            <div className="space-y-2">
              {displayFiles.map((f, i) => (
                <div key={i} className="flex items-center gap-3 p-3 bg-green-50 rounded-xl border border-green-200">
                  <BsFiletypePdf className="text-red-500 text-lg shrink-0" />
                  <span className="text-sm text-green-800 truncate flex-1">{f.name}</span>
                  <button onClick={() => removeResume(i)} className="text-gray-400 hover:text-red-500">
                    <BsXCircle />
                  </button>
                </div>
              ))}
              {extraCount > 0 && (
                <p className="text-xs text-gray-500 pl-2">+ {extraCount} more file{extraCount > 1 ? "s" : ""}</p>
              )}
            </div>
          )}
          {resumeUploading && <p className="text-xs text-blue-600 mt-2">Uploading resumes...</p>}
        </div>
      </div>

      <div className="flex justify-center mt-6">
        <button
          onClick={onEvaluate}
          disabled={!jdUploaded || resumeCount === 0 || evaluating}
          className="px-8 py-3 bg-blue-600 text-white font-semibold rounded-xl text-sm shadow-sm hover:bg-blue-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
        >
          {evaluating ? "Evaluating..." : "Evaluate Candidates"}
        </button>
      </div>
    </div>
  );
}
