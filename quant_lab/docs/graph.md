# The interconnection graph

The portfolio is one connected system, not 72 islands. The 15 sections feed one another
(data → strategies → risk), and they interlock through the mathematics and tools they share,
all sitting on the same data layer. The graph below is the whole thing at once — drag a node,
hover to trace its links.

```{raw} html
<iframe src="_static/graph.html" title="Quant Lab interconnection graph"
        style="width:100%; height:640px; border:1px solid var(--color-background-border,#ccc); border-radius:8px;">
</iframe>
```

How to read it:

- **Sections** (large nodes) are the 15 topic areas.
- Edges to **math/stats** and **technical** nodes show the machinery a section uses; where two
  sections attach to the same node, they share that concept or tool.
- Directed **feeds** edges show the dependency order — e.g. the data infrastructure feeds
  almost everything, and the risk/evaluation backbone is used by every strategy section.

:::{admonition} If the graph doesn't load
:class: note
It's a self-contained interactive page embedded from `_static/graph.html`; open that file
directly in a browser for a full-window view.
:::
