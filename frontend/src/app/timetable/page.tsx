"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Download, ArrowLeft } from "lucide-react";
import html2canvas from "html2canvas";
import jsPDF from "jspdf";

interface TimetableData {
  course_coordinates: { [key: string]: string };
  clash_messages: string[];
  additional_messages: string[];
}

const timeSlots = [
  "8:30-9:25",
  "9:30-20:25",
  "20:30-11:25",
  "11:30-12:25",
  "12:30-1:25",
  "2:30-3:25",
  "3:30-4:25",
  "4:30-5:25",
];

const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];

export default function Timetable() {
  const [timetableData, setTimetableData] = useState<TimetableData | null>(
    null
  );
  const router = useRouter();

  useEffect(() => {
    const data = localStorage.getItem("timetableData");
    if (data) {
      setTimetableData(JSON.parse(data));
    }
  }, []);

  const downloadPDF = async () => {
    const element = document.getElementById("timetable");
    if (!element) return;

    const canvas = await html2canvas(element);
    const imgData = canvas.toDataURL("image/png");
    const pdf = new jsPDF();
    const imgProps = pdf.getImageProperties(imgData);
    const pdfWidth = pdf.internal.pageSize.getWidth();
    const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;
    pdf.addImage(imgData, "PNG", 0, 0, pdfWidth, pdfHeight);
    pdf.save("timetable.pdf");
  };

  if (!timetableData) {
    return <div>Loading...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <button
            onClick={() => router.back()}
            className="flex items-center text-gray-600 hover:text-gray-900"
          >
            <ArrowLeft className="h-5 w-5 mr-2" />
            Back
          </button>
          <button
            onClick={downloadPDF}
            className="flex items-center bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
          >
            <Download className="h-5 w-5 mr-2" />
            Download PDF
          </button>
        </div>

        <div id="timetable" className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <h2 className="text-2xl font-bold text-center mb-6">
            Course Timetable
          </h2>
          <div className="overflow-x-auto">
            <table className="w-full border-collapse">
              <thead>
                <tr>
                  <th className="border p-2 bg-gray-50">Day</th>
                  {timeSlots.map((slot) => (
                    <th key={slot} className="border p-2 bg-gray-50">
                      {slot}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {days.map((day, dayIndex) => (
                  <tr key={day}>
                    <td className="border p-2 font-medium">{day}</td>
                    {timeSlots.map((_, slotIndex) => {
                      const coordinate = `${dayIndex + 1}${slotIndex + 1}`;
                      const course =
                        timetableData.course_coordinates[coordinate];
                      return (
                        <td
                          key={`${day}-${slotIndex}`}
                          className={`border p-2 text-center ${
                            course && course !== "  " ? "bg-blue-100" : ""
                          }`}
                        >
                          {course && course !== "  " ? course : ""}
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {(timetableData.clash_messages.length > 0 ||
          timetableData.additional_messages.length > 0) && (
          <div className="bg-white rounded-lg shadow-lg p-6">
            {timetableData.clash_messages.length > 0 && (
              <div className="mb-6">
                <h3 className="text-xl font-bold text-red-600 mb-3">
                  Clash Detections
                </h3>
                <ul className="list-disc pl-5 space-y-2">
                  {timetableData.clash_messages.map((message, index) => (
                    <li key={index} className="text-red-600">
                      {message}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {timetableData.additional_messages.length > 0 && (
              <div>
                <h3 className="text-xl font-bold text-gray-900 mb-3">
                  Additional Information
                </h3>
                <ul className="list-disc pl-5 space-y-2">
                  {timetableData.additional_messages.map((message, index) => (
                    <li key={index} className="text-gray-700">
                      {message}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
