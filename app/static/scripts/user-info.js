document.addEventListener("DOMContentLoaded", function () {
    const token = sessionStorage.getItem("token");
    console.log("Token from sessionStorage:", token); // Debug log


    if (!token) {
        console.error("No token found in sessionStorage");
        return;
    }

   
fetch("/me/", {
  method: "GET",
  headers: {
    Authorization: `Bearer ${token}`
  }
})
    .then(response => {
        if (!response.ok) {
            console.error("Response status:", response.status); // Debug
            throw new Error("Not authenticated");
        }
        return response.json();
    })
    .then(user => {
        console.log("Fetched user:", user);
        document.getElementById("usernameholder").textContent = user.username;
        document.getElementById("fullName").textContent = user.full_name;
        document.getElementById("role").textContent = user.role;
    })
    .catch(error => {
        console.error("Error fetching user:", error);
    });
});
