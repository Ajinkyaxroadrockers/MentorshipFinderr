const mentorData = document.getElementById("mentor-data");
const mentorList = document.getElementById("mentor-list");
const searchInput = document.getElementById("mentor-search");

const defaultAvatar = "https://ui-avatars.com/api/?name=Mentor&background=0D8ABC&color=fff";
let allMentors = [];

async function fetchMentors() {
  mentorList.innerHTML = '<div class="loading-card">Loading mentors...</div>';

  try {
    const response = await fetch("/api/mentors");
    allMentors = await response.json();
    renderMentors(allMentors);
  } catch (error) {
    mentorList.innerHTML = '<div class="loading-card">Unable to load mentors right now.</div>';
  }
}

function renderMentors(mentors) {
  if (mentors.length === 0) {
    mentorList.innerHTML = `
      <div class="empty-state">
        <i class="bi bi-search"></i>
        <h2>No mentors found</h2>
        <p>Try another search keyword or check again later.</p>
      </div>
    `;
    return;
  }

  mentorList.innerHTML = mentors.map((mentor) => `
    <article class="mentor-card">
      <img
        src="${mentor.image || mentor.photo_path || defaultAvatar}"
        alt="${mentor.name || mentor.mentor_name || "Mentor"}"
        onerror="this.src='${defaultAvatar}'"
      >

      <div class="mentor-info">
        <span class="pill">${mentor.category}</span>
        <h2>${mentor.name || mentor.mentor_name}</h2>
        <p><strong>Branch:</strong> ${mentor.branch}</p>
        <p><strong>Year:</strong> ${mentor.year}</p>
        <p><strong>Expertise:</strong> ${mentor.expertise}</p>
        <p><strong>Email:</strong> ${mentor.email}</p>
        ${mentor.linkedin ? `<p><strong>LinkedIn:</strong> <a href="${mentor.linkedin}" target="_blank">${mentor.linkedin}</a></p>` : ""}
        <a class="primary-btn" href="mailto:${mentor.email}">Contact Mentor</a>
      </div>
    </article>
  `).join("");
}

searchInput.addEventListener("input", () => {
  const keyword = searchInput.value.trim().toLowerCase();

  const filteredMentors = allMentors.filter((mentor) => {
    const name = (mentor.name || mentor.mentor_name || "").toLowerCase();
    const expertise = (mentor.expertise || "").toLowerCase();
    const category = (mentor.category || "").toLowerCase();
    const branch = (mentor.branch || "").toLowerCase();
    const year = (mentor.year || "").toLowerCase();
    const email = (mentor.email || "").toLowerCase();
    const linkedin = (mentor.linkedin || "").toLowerCase();
    const skills = (mentor.skills || []).join(" ").toLowerCase();
    const tags = (mentor.tags || []).join(" ").toLowerCase();

    return (
      name.includes(keyword) ||
      expertise.includes(keyword) ||
      category.includes(keyword) ||
      branch.includes(keyword) ||
      year.includes(keyword) ||
      email.includes(keyword) ||
      linkedin.includes(keyword) ||
      skills.includes(keyword) ||
      tags.includes(keyword)
    );
  });

  renderMentors(filteredMentors);
});

fetchMentors();
