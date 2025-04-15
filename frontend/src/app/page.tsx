"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { ChevronDown, ChevronUp, Search } from "lucide-react";
import { backendDomain } from "../lib/types";
import { Course } from "../lib/types";
import { setTimetable } from "../redux/slices/timetableSlice";
import { arraysEqual } from "../lib/utils";

export default function Home() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [selectedCourses, setSelectedCourses] = useState<number[]>([]);
  const [expandedDisciplines, setExpandedDisciplines] = useState<string[]>([]);
  const [userExpandedDisciplines, setUserExpandedDisciplines] = useState<
    string[]
  >([]);
  const [userCollapsedDisciplines, setUserCollapsedDisciplines] = useState<
    string[]
  >([]);
  const [searchQuery, setSearchQuery] = useState<string>("");
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

  // Filter courses based on search query
  const filteredCourses = useMemo(() => {
    if (searchQuery.trim() === "") return courses;
    return courses.filter(
      (course) =>
        course.course_code.toLowerCase().includes(searchQuery.toLowerCase()) ||
        course.course_name.toLowerCase().includes(searchQuery.toLowerCase())
    );
  }, [searchQuery, courses]);

  // Get unique disciplines from filtered courses
  const disciplines = Array.from(
    new Set(filteredCourses.map((course) => course.discipline))
  );

  // Calculate disciplines with selected courses
  const disciplinesWithSelectedCourses = useMemo(() => {
    return courses
      .filter((course) => selectedCourses.includes(course.id))
      .map((course) => course.discipline)
      .filter(
        (discipline, index, array) => array.indexOf(discipline) === index
      );
  }, [courses, selectedCourses]);

  // Manage expanded disciplines based on search and selection
  useEffect(() => {
    // When searching, override all other settings
    if (searchQuery.trim() !== "") {
      const matchingDisciplines = Array.from(
        new Set(filteredCourses.map((course) => course.discipline))
      );
      if (!arraysEqual(matchingDisciplines, expandedDisciplines)) {
        setExpandedDisciplines(matchingDisciplines);
      }
      return;
    }

    // When not searching, respect user's explicit actions (expanded and collapsed)
    const shouldBeExpanded = [...userExpandedDisciplines];

    // Add disciplines with selected courses, but only if user hasn't explicitly collapsed them
    disciplinesWithSelectedCourses.forEach((discipline) => {
      if (
        !userCollapsedDisciplines.includes(discipline) &&
        !shouldBeExpanded.includes(discipline)
      ) {
        shouldBeExpanded.push(discipline);
      }
    });

    // Apply the changes only if needed
    if (!arraysEqual(shouldBeExpanded, expandedDisciplines)) {
      setExpandedDisciplines(shouldBeExpanded);
    }
  }, [
    searchQuery,
    filteredCourses,
    userExpandedDisciplines,
    userCollapsedDisciplines,
    disciplinesWithSelectedCourses,
    expandedDisciplines,
  ]);

  // Toggle discipline expansion by user action
  const toggleDiscipline = (discipline: string) => {
    if (expandedDisciplines.includes(discipline)) {
      // User is explicitly closing the discipline
      setUserExpandedDisciplines((prev) =>
        prev.filter((d) => d !== discipline)
      );
      setUserCollapsedDisciplines((prev) => [...prev, discipline]);
    } else {
      // User is explicitly opening the discipline
      setUserExpandedDisciplines((prev) => [...prev, discipline]);
      setUserCollapsedDisciplines((prev) =>
        prev.filter((d) => d !== discipline)
      );
    }
  };

  // Toggle course selection
  const toggleCourseSelection = (courseId: number) => {
    setSelectedCourses((prev) => {
      const newSelection = prev.includes(courseId)
        ? prev.filter((id) => id !== courseId)
        : [...prev, courseId];

      // When selecting a course, get its discipline and remove it from collapsed list
      if (!prev.includes(courseId)) {
        const course = courses.find((c) => c.id === courseId);
        if (course) {
          setUserCollapsedDisciplines((prev) =>
            prev.filter((d) => d !== course.discipline)
          );
        }
      }

      return newSelection;
    });
  };

  // Handle clearing search
  const clearSearch = () => {
    setSearchQuery("");
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
      setTimetable(data);
      router.push("/timetable");
    } catch (error) {
      console.error("Error generating timetable:", error);
    }
  };

  const highlightMatch = (text: string, query: string) => {
    if (!query.trim()) return text;

    const regex = new RegExp(`(${query.trim()})`, "gi");
    const parts = text.split(regex);

    return parts.map((part, index) =>
      regex.test(part) ? (
        <span key={index} className="bg-yellow-200">
          {part}
        </span>
      ) : (
        part
      )
    );
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto p-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">
          Course Timetable Generator
        </h1>

        {/* Search Bar */}
        <div className="mb-6 relative">
          <div className="relative">
            <input
              type="text"
              placeholder="Search courses by code or name..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
            <Search className="absolute left-3 top-3.5 h-5 w-5 text-gray-400" />
          </div>
          {searchQuery.trim() !== "" && (
            <button
              onClick={clearSearch}
              className="absolute right-3 top-3 text-sm text-gray-500 hover:text-gray-700"
            >
              Clear
            </button>
          )}
        </div>

        <div className="space-y-4">
          {disciplines.length > 0 ? (
            disciplines.map((discipline) => {
              const disciplineCourses = filteredCourses.filter(
                (course) => course.discipline === discipline
              );
              const selectedCount = disciplineCourses.filter((course) =>
                selectedCourses.includes(course.id)
              ).length;

              // Get total selected in this discipline (including those filtered out)
              const totalSelectedInDiscipline = courses.filter(
                (course) =>
                  course.discipline === discipline &&
                  selectedCourses.includes(course.id)
              ).length;

              return (
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
                      <span className="ml-2 text-sm text-gray-500">
                        ({disciplineCourses.length} courses
                        {totalSelectedInDiscipline > 0 &&
                          `, ${totalSelectedInDiscipline} selected`}
                        )
                      </span>
                    </span>
                    {expandedDisciplines.includes(discipline) ? (
                      <ChevronUp className="h-5 w-5 text-gray-500" />
                    ) : (
                      <ChevronDown className="h-5 w-5 text-gray-500" />
                    )}
                  </button>

                  {expandedDisciplines.includes(discipline) && (
                    <div className="px-4 pb-4">
                      {disciplineCourses.map((course) => (
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
                              {highlightMatch(course.course_code, searchQuery)}
                            </div>
                            <div className="text-sm text-gray-500">
                              {highlightMatch(course.course_name, searchQuery)}
                            </div>
                          </label>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              );
            })
          ) : (
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 text-center">
              <p className="text-gray-600">
                No courses found matching your search criteria.
              </p>
            </div>
          )}
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
