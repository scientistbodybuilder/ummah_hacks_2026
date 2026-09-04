import { useRef, useState, type ReactNode } from "react";
import {
  FileText,
  FolderOpen,
  ScanLine,
  ShieldCheck,
  Sparkles,
  Upload,
  WalletCards,
} from "lucide-react";
import { Button } from "./ui/button";

const Analyze = () => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [fileName, setFileName] = useState("");
  const handleFile = (file?: File) => {
    if (file) setFileName(file.name);
  };
  return (
    <main className="analyze-page">
      <section className="audit-panel gap-2" aria-labelledby="upload-heading">
        <div className="panel-intro">
          <div className="document-icon">
            <FileText />
          </div>
          <div className="intro-copy">
            <div className="title-line">
              <h1 id="upload-heading">Upload Student Loan Agreement</h1>
              <span className="step-pill">Step 1 of 2</span>
            </div>
            {/* <p>
              Automated Shariah Fiqh clause extraction &amp; AAOIFI Standard No.
              8 &amp; 9 compliance check
            </p> */}
          </div>
          <div className="privacy-pill">
            <ShieldCheck /> Zero Data Retention • End-to-End Encrypted
          </div>
        </div>
        <div
          className="drop-zone"
          onDragOver={(event) => event.preventDefault()}
          onDrop={(event) => {
            event.preventDefault();
            handleFile(event.dataTransfer.files[0]);
          }}
        >
          <div className="upload-icon">
            <Upload />
          </div>
          <h2>
            {fileName || (
              <>
                Drag &amp; drop your loan agreement here, or{" "}
                <button
                  type="button"
                  onClick={() => fileInputRef.current?.click()}
                >
                  browse files
                </button>
              </>
            )}
          </h2>
          {fileName && (
            <button
              className="change-file"
              type="button"
              onClick={() => fileInputRef.current?.click()}
            >
              Choose a different file
            </button>
          )}
          <p>
            Upload your Master Promissory Note (MPN), Private Student Loan
            <br className="desktop-break" /> Disclosures, or Income-Share
            Agreement (ISA).
          </p>
          <div className="format-list">
            <span>
              <FileText /> PDF format only
            </span>
            <span>
              <WalletCards /> Up to 30 MB
            </span>
            <span>
              <ScanLine /> Multi-page OCR supported
            </span>
          </div>
          <input
            ref={fileInputRef}
            type="file"
            accept="application/pdf"
            hidden
            onChange={(event) => handleFile(event.target.files?.[0])}
          />
        </div>
        {/* <div className="sample-row">
          <div>
            <Sparkles />
            <strong>Try a sample contract to see an audit:</strong>
          </div>
          <div className="sample-actions">
            <Button
              variant="outline"
              size="sm"
              onClick={() =>
                setFileName("Direct Unsubsidized MPN (2024-25).pdf")
              }
            >
              Direct Unsubsidized MPN (2024-25)
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() =>
                setFileName("Sallie Mae Private Promissory Note.pdf")
              }
            >
              Sallie Mae Private Promissory Note
            </Button>
          </div>
        </div> */}
        <Button disabled={fileName === ""} className='bg-(--accent-color) w-full rounded-md cursor-pointer hover:bg-(--accent-color)/90'>
            Upload
        </Button>
        <div className="feature-grid">
          <Feature icon={<ShieldCheck />} title="AAOIFI Shariah Standards">
            Evaluates Riba al-Nasi'ah, interest capitalization, and default
            penalties against Standard No. 8 &amp; 9.
          </Feature>
          <Feature icon={<ScanLine />} title="Instant Clause Breakdown">
            Processes agreements in under 30 seconds, flagging prohibited,
            conditional, and permissible terms.
          </Feature>
          <Feature icon={<FolderOpen />} title="Exportable Scholarly Memo">
            Generates certified PDF audits with Fiqh citations ready to present
            to Islamic scholars or imams.
          </Feature>
        </div>
      </section>
    </main>
  );
};

function Feature({
  icon,
  title,
  children,
}: {
  icon: ReactNode;
  title: string;
  children: ReactNode;
}) {
  return (
    <div className="feature-item">
      <div className="feature-icon">{icon}</div>
      <div>
        <strong>{title}</strong>
        <p>{children}</p>
      </div>
    </div>
  );
}

export default Analyze;
