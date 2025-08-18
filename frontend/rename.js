async function renameNote(id) {
    const newTitle = prompt("Enter a new name for this note:");
    if (!newTitle) return;
    const res = await fetch(`http://127.0.0.1:8000/rename/${id}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: newTitle })
    });
    if (res.ok) {
        alert('Renamed!');
        location.reload();
    } else {
        alert('Rename failed.');
    }
}

function viewImage(id, type) {
    const url = `http://127.0.0.1:8000/image/${id}/${type}`;
    window.open(url, '_blank');
}
