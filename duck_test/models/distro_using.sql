SELECT
  *
FROM
  {{ source('main', 'linux_distro')}}
WHERE
  name = 'Ubuntu'
