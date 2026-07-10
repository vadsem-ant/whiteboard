# Whiteboard

Draw on an iPad (Apple Pencil, Safari) → tap **Sync** to save the board.

- **App**: https://vadsem-ant.github.io/whiteboard/ (add to Home Screen for full-screen)
- **Boards**: saved to `boards/<name>.png` + `.json` in the **private** repo `vadsem-ant/whiteboard-boards`
- **Auth**: the page needs a fine-grained PAT with *Contents: read & write* on **vadsem-ant/whiteboard-boards** (the private data repo) only
  (Settings → Developer settings → Fine-grained tokens). Enter it once via the ⚙️ panel; it is
  stored in the browser's localStorage.

## Notes

- Finger input is ignored while the pen tool is active (palm rejection); use the Pencil.
  The eraser tool accepts finger input.
- Undo removes the last stroke; Clear wipes the board (with confirmation).
- Multiple boards: change the board name in ⚙️ (e.g. `sketch-1`, `scratch`).
- Commit history = board history.
