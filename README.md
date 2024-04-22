# dot_mngr

WIP

## Update repo

getting newer link providing a link to scrap, wich fit the best with one of the
following scrap techniques:
- apache
- apache_dir
- apache_no_sort
- github
- github_tag
- gitlab
- fossies
- fossies_search
- pypi
- website
- no_scrap

here is a default

```shell
{
	# IN
	"value":		"https://download.savannah.gnu.org/releases/acl",
	"type":			"apache",
	"prefix":		"acl-",
	"suffix":		".tar.gz"

	# OUT
	"link":			""
	"version":		""
}
```

## TODO

1. split repo
1. once finished do:
   1. the doc
   1. test suite
   1. workflows to update repo:
      1. split repo folder into githubs, referencing package as needed, provide
      with template, actions can update repo
