maze_prompt = """
Act as a robot that needs to traverse through the maze.
The maze is presented in a form of 4×6 matrix.
Starting point is (3, 0), finish point is (3, 5).
<rules>
At a time you can move 1 into any direction.
You have to avoid fields with value 1.
Return result in form of a json.
Do not return anything else than a json.

Present consecutive steps following way:
- UP - (1,0)
- DOWN - (-1, 0)
- RIGHT - (0, 1)
- LEFT - (0, -1)
</rules>

Return json in the following structure:
<json_structure>
{
"thinking: "Thinking steps that led to the solution",
"steps": "UP, RIGHT, DOWN, LEFT"
}
</json_structure>

Here is the maze in form of a matrix:
<matrix>
[0,1,0,0,0,0]
[0,0,0,1,0,0]
[0,1,0,1,0,0]
[2,1,0,0,0,2]
<matrix>
"""
