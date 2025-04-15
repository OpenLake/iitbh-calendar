"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { ChevronDown, ChevronUp } from "lucide-react";
import { backendDomain } from "../lib/types";
import { Course } from "../lib/types";

export default function Home() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [selectedCourses, setSelectedCourses] = useState<number[]>([]);
  const [expandedDisciplines, setExpandedDisciplines] = useState<string[]>([]);
  const router = useRouter();

  // Fetch courses when component mounts
  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const response = await fetch(`${backendDomain}/get_all_courses/`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });
        if (!response.ok) {
          console.log("Get All Courses API could not be triggered properly");
          throw new Error(
            "Get All Courses API could not be triggered properly"
          );
        }
        const data = await response.json();
        setCourses(data);
      } catch (error) {
        console.log("Error fetching the courses", error);
      }
    };
    fetchCourses();
  }, []);

  const disciplines = Array.from(
    new Set(courses.map((course) => course.discipline))
  );

  const toggleDiscipline = (discipline: string) => {
    setExpandedDisciplines((prev) =>
      prev.includes(discipline)
        ? prev.filter((d) => d !== discipline)
        : [...prev, discipline]
    );
  };

  const toggleCourseSelection = (courseId: number) => {
    setSelectedCourses((prev) =>
      prev.includes(courseId)
        ? prev.filter((id) => id !== courseId)
        : [...prev, courseId]
    );
  };

  const handleGenerateTimetable = async () => {
    try {
      const response = await fetch(`${backendDomain}/submit/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ course_id_list: selectedCourses }),
      });

      if (!response.ok) {
        console.log("Submit the selections API could not be triggered");
        throw new Error("Submit the selections API could not be triggered");
      }
      const data = await response.json();
      //redux
      router.push("/timetable");
    } catch (error) {
      console.error("Error generating timetable:", error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto p-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">
          Course Timetable Generator
        </h1>

        <div className="space-y-4">
          {disciplines.map((discipline) => (
            <div
              key={discipline}
              className="bg-white rounded-lg shadow-sm border border-gray-200"
            >
              <button
                onClick={() => toggleDiscipline(discipline)}
                className="w-full px-4 py-3 flex items-center justify-between text-left"
              >
                <span className="text-lg font-medium text-gray-900">
                  {discipline}
                </span>
                {expandedDisciplines.includes(discipline) ? (
                  <ChevronUp className="h-5 w-5 text-gray-500" />
                ) : (
                  <ChevronDown className="h-5 w-5 text-gray-500" />
                )}
              </button>

              {expandedDisciplines.includes(discipline) && (
                <div className="px-4 pb-4">
                  {courses
                    .filter((course) => course.discipline === discipline)
                    .map((course) => (
                      <div
                        key={course.id}
                        className="flex items-center space-x-3 py-2"
                      >
                        <input
                          type="checkbox"
                          id={`course-${course.id}`}
                          checked={selectedCourses.includes(course.id)}
                          onChange={() => toggleCourseSelection(course.id)}
                          className="h-4 w-4 text-blue-600 rounded border-gray-300"
                        />
                        <label
                          htmlFor={`course-${course.id}`}
                          className="flex-1 cursor-pointer"
                        >
                          <div className="font-medium text-gray-900">
                            {course.course_code}
                          </div>
                          <div className="text-sm text-gray-500">
                            {course.course_name}
                          </div>
                        </label>
                      </div>
                    ))}
                </div>
              )}
            </div>
          ))}
        </div>

        <button
          onClick={handleGenerateTimetable}
          disabled={selectedCourses.length === 0}
          className="mt-8 w-full bg-blue-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          Generate Timetable
        </button>
      </div>
    </div>
  );
}
