import time

import altair as alt
import pandas as pd
import streamlit as st

from model.ConvoyRobberyModel import ConvoyRobberyModel
from model.City import City

model = st.title("El Botín")
criminal_attack = st.slider(
	"Ataque de los ladrones",
	min_value=1,
	max_value=100,
	value=1,
)
criminal_defense = st.slider(
	"Defensa de los ladrones",
	min_value=1,
	max_value=100,
	value=1,
)
c = City()
c.set_default()
print(c)

height = c.height
width = c.width
model = ConvoyRobberyModel(height, width)


status_text = st.empty()
run = st.button("Run Simulation")


if run:
	tick = time.time()
	step = 0
	# init grid
	df_grid = pd.DataFrame()
	for x in range(width):
		for y in range(height):
			df_grid = pd.concat(
				[df_grid, pd.DataFrame({"x": [x], "y": [y], "agent_count": 0})],
				ignore_index=True,
			)

	heatmap = (
		alt.Chart(df_grid)
		.mark_point(size=100)
		.encode(x="x", y="y", color=alt.Color("agent_count"))
		.interactive()
		.properties(width=800, height=600)
	)

	# init progress bar
	my_bar = st.progress(0, text="Simulation Progress")  # progress
	placeholder = st.empty()
	st.subheader("Agent Grid")
	chart = st.altair_chart(heatmap)

	color_scale = alt.Scale(
		domain=[0, 1, 2, 3, 4], range=["yellow", "salmon", "orange", "crimson", "red"]
	)
	i = 0
	while True:
		model.step()
		for cell in model.grid.coord_iter():
			cell_content, (x, y) = cell
			agent_count = len(cell_content)
			selected_row = df_grid[(df_grid["x"] == x) & (df_grid["y"] == y)]
			df_grid.loc[selected_row.index, "agent_count"] = (
				agent_count  # random.choice([1,2])
			)
		# st.table(df_grid)
		heatmap = (
			alt.Chart(df_grid)
			.mark_circle(size=100)
			.encode(x="x", y="y", color=alt.Color("agent_count", scale=color_scale))
			.interactive()
			.properties(width=800, height=600)
		)
		chart.altair_chart(heatmap)

		time.sleep(1)
		i += 1

	tock = time.time()
	st.success(f"Simulation completed in {tock - tick:.2f} secs")

	# st.subheader('Agent Grid')
	# fig = px.imshow(agent_counts,labels={'color':'Agent Count'})
	# st.plotly_chart(fig)
