const mentorList = document.getElementById("mentor-list");
const searchInput = document.getElementById("mentor-search");

const defaultAvatar = "/static/uploads/default-avatar.svg";

let allMentors = [];

function escapeHtml(value) {
  return String(value || "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

async function fetchMentors() {
  mentorList.innerHTML = '<div class="loading-card">Loading mentors...</div>';

  try {
    const response = await fetch("/api/mentors");

    if (!response.ok) {
      throw new Error("Unable to fetch mentors");
    }

    allMentors = await response.json();
    renderMentors(allMentors);
  } catch (error) {
    mentorList.innerHTML =
      '<div class="loading-card">Unable to load mentors right now.</div>';
  }
}

function renderMentors(mentors) {
  if (mentors.length === 0) {
    mentorList.innerHTML = `
      <div class="empty-state">
        <i class="bi bi-search"></i>
        <h2>No mentors found</h2>
        <p>Try another search keyword.</p>
      </div>
    `;
    return;
  }

  mentorList.innerHTML = mentors
    .map((mentor) => {
      const name = escapeHtml(mentor.mentor_name || "Mentor");
      const branch = escapeHtml(mentor.branch);
      const year = escapeHtml(mentor.year);
      const expertise = escapeHtml(mentor.expertise);
      const email = escapeHtml(mentor.email);
      const linkedin = escapeHtml(mentor.linkedin);

      const image = mentor.photo_path || mentor.image || defaultAvatar;

      return `
      <article class="mentor-card">
        <img
          src="${escapeHtml(image)}"
          alt="${name}"
          onerror="this.onerror=null; this.src='${defaultAvatar}'"
        >

        <div class="mentor-info">
          <h2>${name}</h2>

          <p><strong>Branch:</strong> ${branch}</p>

          <p><strong>Year:</strong> ${year}</p>

          <p><strong>Expertise:</strong> ${expertise}</p>

          <p><strong>Email:</strong> ${email}</p>

          ${
            linkedin
              ? `
            <p>
              <strong>LinkedIn:</strong>
              <a href="${linkedin}" target="_blank" rel="noopener noreferrer">
                ${linkedin}
              </a>
            </p>
          `
              : ""
          }

          <a class="primary-btn" href="mailto:${email}">
            Contact Mentor
          </a>
        </div>
      </article>
    `;
    })
    .join("");
}

searchInput.addEventListener("input", () => {
  const keyword = searchInput.value.trim().toLowerCase();

  const filteredMentors = allMentors.filter((mentor) => {
    const name = (mentor.mentor_name || "").toLowerCase();
    const expertise = (mentor.expertise || "").toLowerCase();
    const branch = (mentor.branch || "").toLowerCase();
    const year = (mentor.year || "").toLowerCase();
    const email = (mentor.email || "").toLowerCase();
    const linkedin = (mentor.linkedin || "").toLowerCase();

    return (
      name.includes(keyword) ||
      expertise.includes(keyword) ||
      branch.includes(keyword) ||
      year.includes(keyword) ||
      email.includes(keyword) ||
      linkedin.includes(keyword)
    );
  });

  renderMentors(filteredMentors);
});

fetchMentors();
