import sentencepiece as spm

def load_sp_model(model_path):
    """Load SentencePiece model from file."""
    sp = spm.SentencePieceProcessor()
    sp.Load(model_path)
    return sp

def encode_sentence(sp_model, sentence):
    """Encode a sentence using SentencePiece."""
    encoded_tokens = sp_model.EncodeAsPieces(sentence)
    token_ids = sp_model.EncodeAsIds(sentence)
    return encoded_tokens, token_ids

def decode_tokens(sp_model, tokens):
    """Decode tokens using SentencePiece."""
    return sp_model.DecodePieces(tokens)

def main():
    # File path to the trained SentencePiece model
    model_path = "data/tok4000.model"

    # Load SentencePiece model
    sp_model = load_sp_model(model_path)

    # Input sentence to encode and decode
    input_sentence = """Server: Republic of Centar after WW3 (Skina konec serverov)
Channel: u-park
Date: 2018-04

bokalce:
:FeelsBadMan: te smeev u eden yt...

bokalce:
epa borjan toa

bokalce:
jas nisto ja neam rodenden

_tosho:
legit neame drug aven iam bez van pravi ja

_tosho:
ez game e

_tosho:
probably

_tosho:
i smeci

bokalce:
predme pocnam i mean

_tosho:
site bea goleming cuck

bokalce:
i ne znam so kur koga postojat

_tosho:
epa po kratko ne cita komstot

_tosho:
znaci ke ti e broken rexyning jop

bokalce:
koga si zemes maener + policst

_tosho:
abe i da go stais frizelechsko

_tosho:
jas legit samo

_tosho:
wait

bokalce:
xd

bokalce:
xd

bokalce:
dude

_tosho:
sega spiev u 19:20"""

    # Print the number of words in the sentence
    num_words = len(input_sentence.split())
    print("Number of words in the sentence:", num_words)

    # Encode the input sentence
    encoded_tokens, token_ids = encode_sentence(sp_model, input_sentence)

    # Separate arrays for tokens and token IDs
    tokens_array = []
    token_ids_array = []
    for token, token_id in zip(encoded_tokens, token_ids):
        tokens_array.append(token)
        token_ids_array.append(token_id)

    # Print the arrays separately
    print("Tokens:", tokens_array)
    print("Token IDs:", token_ids_array)

    # Print the number of tokens
    num_tokens = len(encoded_tokens)
    print("Number of tokens in the sentence:", num_tokens)

    # Decode the encoded tokens
    decoded_sentence = decode_tokens(sp_model, encoded_tokens)
    print("Decoded sentence:", decoded_sentence)

if __name__ == "__main__":
    main()