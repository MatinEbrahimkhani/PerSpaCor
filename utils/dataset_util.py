import numpy as np


def summery_chunked(input_ids_list, attention_mask_list, labels_list, show_data=False):
    def count_unique_types(two_d_list):
        unique_types = set()
        for sublist in two_d_list:
            for item in sublist:
                unique_types.add(type(item))
        return unique_types

    mask_shape = np.array(attention_mask_list).shape
    ids_shape = np.array(input_ids_list).shape
    lbl_shape = np.array(labels_list).shape
    print("Shapes\nIDs:\t\t\t", ids_shape)
    print("Labels:\t\t\t", lbl_shape)
    print("Attention Mask:\t", mask_shape)

    # Example usage:
    if show_data:
        print(f'input_ids\n{np.array(input_ids_list)}\n',
              f'labels_list\n{np.array(labels_list)}\n\n',
              f'attention_mask_list\n{np.array(attention_mask_list)}\n\n',
              f'Unique types in input_ids_list: {count_unique_types(input_ids_list)}\n\n',
              f'Unique types in labels_list: {count_unique_types(labels_list)}\n\n',
              f'Unique types in attention_mask_list: {count_unique_types(attention_mask_list)}\n\n')


def chunk_pad_tokens(tokens, labels, chunk_size=512, tok_pad=0, label_pad=-100, attention_pad=0, summary=False):
    input_ids_list = []
    attention_mask_list = []
    labels_list = []

    # Create chunks
    for i in range(0, len(tokens), chunk_size):  # We subtract 2 to account for special tokens
        chunked_tokens = tokens[i:i + chunk_size]
        chunk_attention_mask = [1] * len(chunked_tokens)
        chunk_label_ids = labels[i:i + chunk_size]

        while len(chunked_tokens) < chunk_size:
            chunked_tokens.append(0)
            chunk_attention_mask.append(0)
            chunk_label_ids.append(-100)
        input_ids_list.append(chunked_tokens)
        attention_mask_list.append(chunk_attention_mask)
        labels_list.append(chunk_label_ids)
    if summary:
        summery_chunked(input_ids_list, attention_mask_list, labels_list, False)
    return input_ids_list, attention_mask_list, labels_list


def remove_large_elements(lst, threshold):
    for i in range(len(lst)):
        lst[i] = [x for x in lst[i] if len(str(x)) <= threshold]
    return lst


class Dataset_Builder:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        pass

    def chunck_tokens(self, tokens, labels, chunk_size=512, summery=False):
        input_ids_list = []
        attention_mask_list = []
        labels_list = []

        # Create chunks
        for i in range(0, len(tokens), 512 - 2):  # We subtract 2 to account for special tokens
            chunk_tokens = tokens[i:i + 512 - 2]
            chunk_label_ids = labels[i:i + 512 - 2]

            # Add special tokens
            chunk_tokens = [self.tokenizer.encode('[CLS]')[1]] + chunk_tokens + [self.tokenizer.encode('[SEP]')[1]]
            # chunk_tokens = ['[CLS]'] + chunk_tokens + ['[SEP]']
            chunk_label_ids = [-100] + chunk_label_ids + [-100]

            # Convert tokens to input IDs and create attention mask

            chunk_attention_mask = [1] * len(chunk_tokens)

            # Pad sequenceschunk_input_ids = tokenizer.convert_tokens_to_ids(chunk_tokens)
            while len(chunk_tokens) < chunk_size:
                chunk_tokens.append(0)
                chunk_attention_mask.append(0)
                chunk_label_ids.append(-100)

            input_ids_list.append(chunk_tokens)
            attention_mask_list.append(chunk_attention_mask)
            labels_list.append(chunk_label_ids)
        if summery:
            self.summery_chuncked(input_ids_list, attention_mask_list, labels_list)
        return input_ids_list, attention_mask_list, labels_list

    @staticmethod
    def summery_chuncked(input_ids_list, attention_mask_list, labels_list, show_data=False):
        def count_unique_types(two_d_list):
            unique_types = set()
            for sublist in two_d_list:
                for item in sublist:
                    unique_types.add(type(item))
            return unique_types

        mask_shape = np.array(attention_mask_list).shape
        ids_shape = np.array(input_ids_list).shape
        lbl_shape = np.array(labels_list).shape
        print("Shapes\nIDs:\t\t\t", ids_shape)
        print("Labels:\t\t\t", lbl_shape)
        print("Attention Mask:\t", mask_shape)

        # Example usage:
        if show_data:
            print('input_ids\n', np.array(input_ids_list))
            print('\n\n\n\nlabels_list\n', np.array(labels_list))
            print('\n\n\n\nattention_mask_list\n', np.array(attention_mask_list))
            print(count_unique_types(input_ids_list))  # Output: 4
            print(lbl_shape, count_unique_types(labels_list))  # Output: 4
            print(mask_shape, count_unique_types(attention_mask_list))  # Output: 4
