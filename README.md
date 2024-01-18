# Todo List with HTMX
Just experimenting with `htmx` ..

- [-] Create: Only blank row created right now, entered values won't persist.
- [x] Read
- [ ] Update
- [-] Delete: WIP


## TODO
- Exclude `testing.py` from server restart in Flask debug mode.
- Fix Delete functionality: it deletes *some row* but not necessarily the right one (HTMX front-end issue).
  Current implementation is hacky, replace it with real implementation like
  [this example](https://htmx.org/examples/delete-row/).