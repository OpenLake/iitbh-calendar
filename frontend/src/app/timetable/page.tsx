"use client";

import { useRouter } from "next/navigation";
import { Download, ArrowLeft } from "lucide-react";
import html2canvas from "html2canvas";
import jsPDF from "jspdf";
import { timeSlots } from "@/src/lib/types";
import { days } from "@/src/lib/types";
import { useSelector } from "react-redux";
import { RootState } from "@/src/redux/store";
import { clearTimetable } from "@/src/redux/slices/timetableSlice";
import { isNotCourse } from "@/src/lib/utils";
import { useEffect, useState } from "react";
import { useDispatch } from "react-redux";

export default function Timetable() {
  const router = useRouter();
  const dispatch = useDispatch();
  const { mapping, clashes, additional_messages } = useSelector(
    (state: RootState) => state.timetable
  );

  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    // This ensures we only log after the Redux store has been rehydrated
    setIsLoaded(true);
    console.log("Timetable state:", { mapping, clashes, additional_messages });
  }, [mapping, clashes, additional_messages]);

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

  const handleBack = () => {
    dispatch(clearTimetable());
    router.back();
  };

  if (!isLoaded || !mapping || Object.keys(mapping).length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading timetable data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <button
            onClick={handleBack}
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
                      const course = mapping[coordinate];
                      return (
                        <td
                          key={`${day}-${slotIndex}`}
                          className={`border p-2 text-center ${
                            course && !isNotCourse(course) ? "bg-blue-500" : ""
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
        {
          <div className="bg-white rounded-lg shadow-lg p-6">
            <div className="mb-6">
              <h3 className="text-xl font-bold text-red-600 mb-3">
                Clash Detections
              </h3>
              {clashes && clashes.length > 0 ? (
                <ul className="list-disc pl-5 space-y-2">
                  {clashes.map((message, index) => (
                    <li key={index} className="text-red-600">
                      {message}
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-gray-600">No clashes detected.</p>
              )}
            </div>

            <div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">
                Additional Information
              </h3>
              {additional_messages && additional_messages.length > 0 ? (
                <ul className="list-disc pl-5 space-y-2">
                  {additional_messages.map((message, index) => (
                    <li key={index} className="text-gray-700">
                      {message}
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-gray-600">No additional information.</p>
              )}
            </div>
          </div>
        }
      </div>
    </div>
  );
}
