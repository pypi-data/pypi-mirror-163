# zenutils

Collection of simple utils. No extra packages required.

## Install

```
pip install zenutils
```

## Utils

1. zenutils.base64utils
    1. a85decode
    1. a85encode
    1. b16decode
    1. b16encode
    1. b32decode
    1. b32encode
    1. b32hexdecode
    1. b32hexencode
    1. b64decode
    1. b64encode
    1. b85decode
    1. b85encode
    1. decode
    1. decodebytes
    1. encode
    1. encodebytes
    1. standard_b64decode
    1. standard_b64encode
    1. urlsafe_b64decode
    1. urlsafe_b64encode
1. zenutils.baseutils
    1. Null
1. zenutils.cacheutils
    1. get_cached_value
1. zenutils.cipherutils
    1. Base64Encoder
    1. CipherBase
    1. DecryptFailed
    1. EncoderBase
    1. HexlifyEncoder
    1. IvCipher
    1. IvfCipher
    1. MappingCipher
    1. RawDataEncoder
    1. S12Cipher
    1. S1Cipher
    1. S2Cipher
    1. SafeBase64Encoder
    1. Utf8Encoder
1. zenutils.dictutils
    1. Object
    1. attrgetorset
    1. attrset
    1. change
    1. changes
    1. deep_merge
    1. diff
    1. fix_object
    1. ignore_none_item
    1. prefix_key
    1. select
    1. to_object
    1. touch
    1. update
1. zenutils.fsutils
    1. TemporaryFile
    1. copy
    1. expand
    1. file_content_replace
    1. filecopy
    1. first_exists_file
    1. get_application_config_filepath
    1. get_application_config_paths
    1. get_size_deviation
    1. get_size_display
    1. get_temp_workspace
    1. get_unit_size
    1. info
    1. mkdir
    1. move
    1. pathjoin
    1. readfile
    1. rename
    1. rm
    1. size_unit_names
    1. size_unit_upper_limit
    1. touch
    1. treecopy
    1. write
1. zenutils.funcutils
    1. BunchCallable
    1. call_with_inject
    1. chain
    1. classproperty
    1. get_all_builtin_exceptions
    1. get_builtins_dict
    1. get_class_name
    1. get_default_values
    1. get_inject_params
    1. is_a_class
    1. mcall_with_inject
    1. signature
    1. try_again_on_error
1. zenutils.hashutils
    1. get_file_hash
    1. get_file_md5
    1. get_file_sha
    1. get_file_sha1
    1. get_file_sha224
    1. get_file_sha256
    1. get_file_sha384
    1. get_file_sha512
    1. get_hash_base64
    1. get_hash_hexdigest
    1. get_md5
    1. get_md5_base64
    1. get_md5_hexdigest
    1. get_password_hash
    1. get_password_hash_methods
    1. get_pbkdf2_hmac
    1. get_pbkdf2_md5
    1. get_pbkdf2_sha
    1. get_pbkdf2_sha1
    1. get_pbkdf2_sha224
    1. get_pbkdf2_sha256
    1. get_pbkdf2_sha384
    1. get_pbkdf2_sha512
    1. get_sha
    1. get_sha1
    1. get_sha1_base64
    1. get_sha1_hexdigest
    1. get_sha224
    1. get_sha224_base64
    1. get_sha224_hexdigest
    1. get_sha256
    1. get_sha256_base64
    1. get_sha256_hexdigest
    1. get_sha384
    1. get_sha384_base64
    1. get_sha384_hexdigest
    1. get_sha512
    1. get_sha512_base64
    1. get_sha512_hexdigest
    1. get_sha_base64
    1. get_sha_hexdigest
    1. method_load
    1. pbkdf2_hmac
    1. register_password_hash_method
    1. validate_password_hash
    1. validate_pbkdf2_hmac
    1. validate_pbkdf2_md5
    1. validate_pbkdf2_sha
    1. validate_pbkdf2_sha1
    1. validate_pbkdf2_sha224
    1. validate_pbkdf2_sha256
    1. validate_pbkdf2_sha384
    1. validate_pbkdf2_sha512
1. zenutils.httputils
    1. download
    1. get_sitename
    1. get_url_filename
    1. get_url_save_path
    1. get_urlinfo
    1. urlparse
1. zenutils.jsonutils
    1. SimpleJsonEncoder
    1. make_simple_json_encoder
    1. register_global_encoder
    1. simple_json_dumps
1. zenutils.listutils
    1. append_new
    1. chunk
    1. clean_none
    1. compare
    1. compare_execute
    1. first
    1. group
    1. ignore_none_element
    1. int_list_to_bytes
    1. is_ordered
    1. list2dict
    1. pad
    1. replace
    1. topological_sort
    1. topological_test
    1. unique
1. zenutils.logutils
    1. get_console_handler
    1. get_file_handler
    1. get_simple_config
    1. setup
1. zenutils.nameutils
    1. get_last_names
    1. get_random_name
    1. get_suggest_first_names
    1. guess_lastname
    1. guess_surname
1. zenutils.numericutils
    1. _infinity
    1. binary_decompose
    1. bytes2ints
    1. decimal_change_base
    1. float_split
    1. from_bytes
    1. get_float_part
    1. infinity
    1. int2bytes
    1. ints2bytes
    1. is_infinity
    1. ninfinity
    1. pinfinity
1. zenutils.randomutils
    1. Random
    1. UuidGenerator
    1. choices
    1. uuid1
    1. uuid3
    1. uuid4
    1. uuid5
1. zenutils.sixutils
    1. BASESTRING_TYPES
    1. BYTES
    1. BYTES_TYPE
    1. INT_TO_BYTES
    1. NUMERIC_TYPES
    1. PY2
    1. PY3
    1. STR_TYPE
    1. TEXT
    1. bchar
    1. bstr_to_array
    1. bytes_to_array
    1. default_encoding
    1. default_encodings
    1. force_bytes
    1. force_text
1. zenutils.strutils
    1. BAI
    1. BASE64_CHARS
    1. HEXLIFY_CHARS
    1. QIAN
    1. SHI
    1. URLSAFEB64_CHARS
    1. WAN
    1. YI
    1. binarify
    1. bytes2ints
    1. camel
    1. captital_number
    1. char_force_to_int
    1. chunk
    1. clean
    1. combinations
    1. combinations2
    1. decodable
    1. default_cn_digits
    1. default_cn_float_places
    1. default_cn_negative
    1. default_cn_places
    1. default_cn_yuan
    1. default_encoding
    1. default_encodings
    1. default_quotes
    1. default_random_string_choices
    1. do_clean
    1. encodable
    1. force_float
    1. force_int
    1. force_numberic
    1. force_type_to
    1. format_with_mapping
    1. get_all_substrings
    1. get_base64image
    1. get_image_bytes
    1. html_element_css_append
    1. int2bytes
    1. ints2bytes
    1. is_base64_decodable
    1. is_chinese_character
    1. is_hex_digits
    1. is_str_composed_by_the_choices
    1. is_unhexlifiable
    1. is_urlsafeb64_decodable
    1. is_uuid
    1. join_lines
    1. no_mapping
    1. none_to_empty_string
    1. parse_base64image
    1. random_string
    1. remove_prefix
    1. remove_suffix
    1. reverse
    1. simplesplit
    1. smart_get_binary_data
    1. split
    1. split2
    1. str_composed_by
    1. stringlist_append
    1. strip_string
    1. substrings
    1. text_display_length
    1. text_display_shorten
    1. unbinarify
    1. unquote
    1. wholestrip
1. zenutils.sysutils
    1. default_timeout_kill
    1. execute_script
    1. get_current_thread_id
    1. get_node_ip
    1. get_random_script_name
    1. get_worker_id
    1. psutil_timeout_kill
1. zenutils.threadutils
    1. Counter
    1. LoopIdle
    1. Service
    1. ServiceStop
    1. ServiceTerminate
    1. SimpleConsumer
    1. SimpleProducer
    1. SimpleProducerConsumerServer
    1. SimpleServer
    1. StartOnTerminatedService
1. zenutils.treeutils
    1. SimpleRouterTree
    1. build_tree
    1. print_tree
    1. print_tree_callback
    1. tree_walk
1. zenutils.typingutils
    1. Number
    1. STRING_ENCODINGS
    1. register_global_caster
    1. smart_cast

## Compatibility

Test passed with python versions:

1. Python 2.7 passed
1. Python 3.2 passed
1. Python 3.3 passed
1. Python 3.4 passed
1. Python 3.5 passed
1. Python 3.7 passed
1. Python 3.8 passed
1. Python 3.9 passed
1. Python 3.10 passed

## Release

### v0.1.0

- First release.

### v0.2.0

- Add treeutils.SimpleRouterTree.
- Add randomutils.HashPrng.
- Add hashutils.get_password_hash and hashutils.validate_password_hash.
- Add dictutils.HttpHeadersDict.
- Add sysutils.get_node_ip.

### v0.3.1

- Add funcutils.retry.
- Fix hashutils.validate_password_hash problem.
