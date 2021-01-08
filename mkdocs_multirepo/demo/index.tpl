<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Multirepo Demo Page</title>
    <link rel="stylesheet" type="text/css" href="styles.css">
</head>

<body>
    <div class="search-container">
        <h1 class="search-greeting">
            <div class="search-greeting-logo-container">
                <img class="search-greeting-logo" src="images/search.svg" title="Logo">
            </div>
            <div>How can we help you?</div>
        </h1>
        <form class="search-form" action="" id="search-form" role="search">
            <input class="search-input" placeholder="Describe your issue" autocomplete="off" name="q" spellcheck="false"
                type="search">
            <button class="search-search-button">
                <svg class="search-search-icon" viewBox="0 0 24 24">
                    <path
                        d="M20.49 19l-5.73-5.73C15.53 12.2 16 10.91 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.41 0 2.7-.47 3.77-1.24L19 20.49 20.49 19zM5 9.5C5 7.01 7.01 5 9.5 5S14 7.01 14 9.5 11.99 14 9.5 14 5 11.99 5 9.5z">
                    </path>
                </svg>
            </button>
        </form>
    </div>

    <div class="tiles-container">
        <section id="multirepo">
        </section>
    </div>
</body>

</html>