import os
from dotenv import load_dotenv

from livekit.agents import (
    AgentSession,
    AutoSubscribe,
    JobContext,
    WorkerOptions,
    cli,
)
from livekit.agents.voice import Agent
from livekit.plugins import openai, silero


load_dotenv()


async def entrypoint(ctx: JobContext):
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    print("Voice agent connected to room")

    # Create the agent session with the models
    session = AgentSession(
        vad=silero.VAD.load(),  # Add VAD for non-streaming STT
        stt=openai.STT(model="gpt-4o-transcribe"),
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=openai.TTS(model="gpt-4o-mini-tts", voice="alloy"),
    )

    # Create the agent with instructions
    agent = Agent(
        instructions="You are Greva, a polite and concise voice assistant.",
    )

    # Start the session with the agent and room
    await session.start(agent=agent, room=ctx.room)

    # Generate a greeting
    await session.generate_reply(instructions="Greet the user warmly and introduce yourself as Greva")


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
        )
    )
