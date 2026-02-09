document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form[data-dirty-tracker='true']");
  const statusEl = document.getElementById("live-status");

  if (!form || !statusEl) return;

  let isDirty = false;

  const setUnsaved = () => {
    if (isDirty) return;
    isDirty = true;
    statusEl.textContent = "YOUR CHANGES ARE NOT SAVED!";
    statusEl.classList.remove("status-saved", "status-saving");
    statusEl.classList.add("status-unsaved");
  };

  form.addEventListener("input", setUnsaved);
  form.addEventListener("change", setUnsaved);

  form.addEventListener("submit", () => {
    statusEl.textContent = "Saving...";
    statusEl.classList.remove("status-unsaved", "status-saved");
    statusEl.classList.add("status-saving");
  });
});
