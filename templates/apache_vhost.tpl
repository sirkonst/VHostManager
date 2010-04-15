<VirtualHost *>
	ServerName      $sitename
	ServerAlias     ${site_aliases}

	DocumentRoot	"$docroot"

	AssignUserID	$username $username
	MaxClientsVHost	$maxclients

	# Переадресация на домены с www. в начале согласно ServerName.
	# Без 'UseCanonicalName On' работать нее будет
	RewriteEngine	on
	RewriteCond	%%{HTTP_HOST} !^www\.
	RewriteRule	^(.*)$$ http://%%{SERVER_NAME}$$1 [R=301,L]

	<Directory "$docroot">
		AllowOverride All

		Order allow,deny
		Allow from all
	</Directory>
</VirtualHost>

