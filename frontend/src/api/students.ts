import { api } from "./client";

export interface StudentCourse {
  id: number;
  course_name: string;
  credits: number | null;
  grade: string | null;
  semester_taken: string | null;
}

export interface StudentProfile {
  user_id: number;
  full_name: string | null;
  education_level: string | null;
  program: string | null;
  semester: number | null;
  gpa: number | null;
  updated_at: string;
  courses: StudentCourse[];
}

export function getStudentProfile(): Promise<StudentProfile> {
  return api<StudentProfile>("/api/students/me");
}

/**
 * Update student profile (name, education level, program).
 */
export function updateStudentProfile(
  full_name?: string,
  education_level?: string,
  program?: string,
): Promise<StudentProfile> {
  const body: Record<string, string | null> = {};
  if (full_name !== undefined) body.full_name = full_name || null;
  if (education_level !== undefined) body.education_level = education_level || null;
  if (program !== undefined) body.program = program || null;
  return api<StudentProfile>("/api/students/profile", {
    method: "PUT",
    json: body,
  });
}

/**
 * Upload a transcript PDF. Processing runs in a background worker, so this
 * returns a job id immediately (HTTP 202). Poll the job (see `pollJob` in
 * `./jobs`) and refetch the profile with `getStudentProfile` once it succeeds.
 */
export function uploadTranscript(
  file: File,
  program?: string,
  semester?: number,
): Promise<{ job_id: string }> {
  const fd = new FormData();
  fd.append("file", file);
  if (program) fd.append("program", program);
  if (semester != null) fd.append("semester", String(semester));
  return api<{ job_id: string }>("/api/students/me/transcript", {
    method: "POST",
    multipart: fd,
  });
}
