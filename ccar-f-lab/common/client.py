"""Shared client factory. --offline returns a scripted mock so loops can be studied without a key."""
import os, sys, json, types
MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5")
OFFLINE = "--offline" in sys.argv

class _Block(types.SimpleNamespace): pass
class MockMessages:
    """Replays a script: list of responses, each a dict(stop_reason, content=[blocks])."""
    def __init__(self, script): self.script, self.i = script, 0
    def create(self, **kw):
        r = self.script[min(self.i, len(self.script)-1)]; self.i += 1
        content = [_Block(**b) for b in r["content"]]
        return types.SimpleNamespace(stop_reason=r["stop_reason"], content=content,
                                     usage=types.SimpleNamespace(input_tokens=0, output_tokens=0))

def get_client(mock_script=None):
    if OFFLINE:
        return types.SimpleNamespace(messages=MockMessages(mock_script or []))
    import anthropic
    return anthropic.Anthropic()

def text_of(resp):
    return "".join(getattr(b, "text", "") for b in resp.content if b.type == "text")
