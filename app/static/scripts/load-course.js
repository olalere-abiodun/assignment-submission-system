document.addEventListener("DOMContentLoaded", function () {
  const token = sessionStorage.getItem("token");
  const formMessages = document.getElementById("form-messages");

  if (!token) {
    showMessage("No token found. Redirecting to login...", "danger");
    window.location.href = "../login.html";
    return;
  }

  const select = document.getElementById("course_title");
  const courseCodeInput = document.getElementById("course_code");
  const form = document.getElementById("enrollForm");

  function showMessage(message, type = "info") {
    formMessages.textContent = message;
    formMessages.className = `alert alert-${type}`;
    formMessages.classList.remove("d-none");
  }

  // Load courses
  fetch("/courses/", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
    .then(response => {
      if (response.status === 401) throw new Error("Not authenticated. Please login again.");
      if (!response.ok) throw new Error("Failed to fetch courses");
      return response.json();
    })
    .then(courses => {
      console.log("Fetched courses:", courses);
      select.length = 1; // keep only the first option

      courses.forEach(course => {
        const option = document.createElement("option");
        option.value = course.course_id;
        option.textContent = course.course_name;
        option.setAttribute("data-code", course.course_code);
        select.appendChild(option);
      });
    })
    .catch(error => {
      console.error("Error loading courses:", error);
      showMessage(error.message, "danger");
      if (error.message.includes("Not authenticated")) {
        setTimeout(() => window.location.href = "/login.html", 1500);
      }
    });

  // Update course code on select change
  select.addEventListener("change", function () {
    const selectedOption = select.options[select.selectedIndex];
    const courseCode = selectedOption.getAttribute("data-code");
    courseCodeInput.value = courseCode || "";
  });

  // Handle form submission
  form.addEventListener("submit", function (e) {
    e.preventDefault();

    const courseId = select.value;
    if (!courseId) {
      showMessage("Please select a course", "warning");
      return;
    }

    fetch(`/courses/${courseId}/enroll`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
      .then(response => {
        if (response.status === 401) throw new Error("Not authenticated. Please login again.");
        if (!response.ok) {
          return response.json().then(data => {
            throw new Error(data.detail || "Enrollment failed");
          });
        }
        return response.json();
      })
      .then(data => {
        showMessage(`✅ Enrolled successfully in ${data.course_name} (${data.course_code})`, "success");
        form.reset();
        courseCodeInput.value = "";
      })
      .catch(error => {
        console.error("Enrollment error:", error);
        showMessage("❌ " + error.message, "danger");
        if (error.message.includes("Not authenticated")) {
          setTimeout(() => window.location.href = "/login.html", 1500);
        }
      });
  });
});
