async function fetchNotes() {
    const res = await fetch('http://127.0.0.1:8000/list');
    if (!res.ok) {
        document.getElementById('notes-list').innerHTML = '<p>Failed to load notes.</p>';
        return;
    }
    const notes = await res.json();
    renderNotes(notes);
}

function renderNotes(notes) {

    const list = document.getElementById('notes-list');
    if (!notes.length) {
        list.innerHTML = '<p>No notes found.</p>';
        return;
    }
    list.innerHTML = '';
    notes.forEach(note => {
        const card = document.createElement('div');
        card.className = 'note-card';
        card.innerHTML = `
            <div class="note-title">${note.meta.title || note.id}</div>
            <div class="note-meta">${Object.entries(note.meta).map(([k,v]) => `<b>${k}:</b> ${v}`).join(' | ')}</div>
            <div style="margin-bottom:8px; position:relative;">
                <img id="img-${note.id}" src="http://127.0.0.1:8000/image/${note.id}/cropped" alt="cropped" style="max-width:180px;max-height:120px;cursor:pointer;border:1px solid #ccc;border-radius:4px;transition:transform 0.2s;" onclick="viewImage('${note.id}','cropped')">
                <button style="position:absolute;top:4px;right:4px;z-index:2;" onclick="event.stopPropagation(); rotateImage('${note.id}')">⟳</button>
            </div>
            <button onclick="renameNote('${note.id}')">Rename</button>
        `;
        list.appendChild(card);
    });
}


// Add rotateImage function to window (only backend rotation, persistent)
window.rotateImage = async function(id) {
    await fetch(`http://127.0.0.1:8000/rotate/${id}`, {method: 'POST'});
    const img = document.getElementById('img-' + id);
    img.src = `http://127.0.0.1:8000/image/${id}/cropped?${Date.now()}`;
}

document.addEventListener('DOMContentLoaded', fetchNotes);
